import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3
import argparse

class MiniCrawler:
    def __init__(self, api_url="http://localhost:8000/index"):
        self.api_url = api_url
        self.visited = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def crawl(self, start_url, max_pages=10):
        queue = [start_url]
        count = 0

        print(f"Starting crawl at: {start_url}")
        print(f"Target API: {self.api_url}\n")

        while queue and count < max_pages:
            url = queue.pop(0)
            if url in self.visited:
                continue

            try:
                # 1. Fetch the page
                response = requests.get(url, timeout=5, verify=False, headers=self.headers)

                if response.status_code != 200:
                    print(f"Skipping {url}: Status Code {response.status_code}")
                    continue
                
                self.visited.add(url)

                # 2. Parse HTML and extract clean text
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove non-content elements
                for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
                    script_or_style.decompose()

                clean_text = soup.get_text(separator=' ').strip()
                
                if not clean_text:
                    continue

                # 3. Generate a consistent Integer ID
                # Using abs(hash) ensures we stay within C++ int limits
                doc_id = abs(hash(url)) % (10**8)

                # 4. Post to the Hybrid Engine API
                payload = {"id": doc_id, "content": clean_text}
                api_res = requests.post(self.api_url, json=payload)

                if api_res.status_code == 200:
                    status = api_res.json().get("status")
                    print(f"[{count+1}/{max_pages}] Indexed: {url} (ID: {doc_id}) - {status}")
                else:
                    print(f"Failed to index {url}: {api_res.text}")

                # 5. Extract internal links for the queue
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    # Only stay on the same domain to avoid crawling the whole internet
                    if urlparse(full_url).netloc == urlparse(start_url).netloc:
                        if full_url not in self.visited:
                            queue.append(full_url)
                
                count += 1

            except Exception as e:
                print(f"Error crawling {url}: {e}")

        print(f"\n Crawl finished. Total pages indexed: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://example.com", help="The starting URL to crawl")
    parser.add_argument("--pages", type=int, default=5, help="Maximum number of pages to crawl")
    args = parser.parse_args()

    crawler = MiniCrawler()
    crawler.crawl(args.url, max_pages=args.pages)