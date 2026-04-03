# hybrid-search-engine

## Summary
This project is a high-performance Information Retrieval (IR) System that demonstrates the "Real-World" approach of combining Python's development speed with C++'s execution power. It covers the entire lifecycle of data: from crawling raw HTML on the web to serving ranked results in a modern UI.

## 🛠 The Technical Stack
**Core Engine:** C++20 (Inverted Index, TF-IDF, Cosine Similarity).

**Bridge:** Pybind11 (Connecting C++ logic to Python).

**API & Backend:** FastAPI (Python), NLTK (NLP Preprocessing).

**Ingestion:** Python Web Crawler & BeautifulSoup4 (HTML Parsing).

**DevOps:** Docker (Multi-stage builds) and Pytest.

**Frontend:** Tailwind CSS & Vanilla JavaScript.

## Getting Started
### 1. Build (Docker)
```
# Build the image
docker build -t search-engine .

# Run the container
docker run -d -p 8000:8000 --name search-app search-engine
```