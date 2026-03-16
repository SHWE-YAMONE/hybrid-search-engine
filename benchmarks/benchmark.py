import time
import random
import string
import numpy as np
import matplotlib.pyplot as plt
from preprocessing.preprocess import clean_text
import fast_search 

# 1. Pure Python Implementation for Comparison
class PythonSearchEngine:
    def __init__(self):
        self.index = {}
        self.doc_norms = {}
        self.total_docs = 0

    def index_document(self, doc_id, tokens):
        self.total_docs += 1
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        
        sum_sq = 0
        for term, freq in counts.items():
            if term not in self.index:
                self.index[term] = []
            self.index[term].append((doc_id, freq))
            sum_sq += freq ** 2
        self.doc_norms[doc_id] = np.sqrt(sum_sq)

    def search(self, query_tokens):
        scores = {}
        for term in query_tokens:
            if term in self.index:
                # IDF calculation
                idf = np.log(self.total_docs / len(self.index[term]))
                for doc_id, freq in self.index[term]:
                    scores[doc_id] = scores.get(doc_id, 0) + (freq * idf) * (1.0 * idf)
        
        results = []
        for doc_id, score in scores.items():
            results.append((doc_id, score / (self.doc_norms[doc_id] + 1e-9)))
        return sorted(results, key=lambda x: x[1], reverse=True)

# 2. Synthetic Data Generator
def generate_fake_data(num_docs=1000, words_per_doc=50):
    vocab = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(500)]
    dataset = {}
    for i in range(num_docs):
        content = " ".join(random.choices(vocab, k=words_per_doc))
        dataset[i] = content
    return dataset, vocab

# 3. Execution 
if __name__ == "__main__":
    print("Generating synthetic dataset (10,000 documents)...")
    data, vocab = generate_fake_data(num_docs=10000)
    
    py_engine = PythonSearchEngine()
    cpp_engine = fast_search.SearchEngine()

    # Benchmark Indexing
    print("Indexing...")
    start = time.time()
    for doc_id, text in data.items():
        tokens = text.split() # Skip heavy NLP for raw speed test
        py_engine.index_document(doc_id, tokens)
    py_index_time = time.time() - start

    start = time.time()
    for doc_id, text in data.items():
        tokens = text.split()
        cpp_engine.index_document(doc_id, tokens)
    cpp_index_time = time.time() - start

    # Benchmark Searching
    queries = [random.choices(vocab, k=2) for _ in range(100)]
    
    print("Searching (100 queries)...")
    start = time.time()
    for q in queries:
        py_engine.search(q)
    py_search_time = (time.time() - start) / 100

    start = time.time()
    for q in queries:
        cpp_engine.search(q)
    cpp_search_time = (time.time() - start) / 100

    # 4. Results
    print("\n" + "="*30)
    print(f"{'Metric':<20} | {'Python':<10} | {'C++ Hybrid':<10}")
    print("-" * 45)
    print(f"{'Indexing (s)':<20} | {py_index_time:10.4f} | {cpp_index_time:10.4f}")
    print(f"{'Search Latency (s)':<20} | {py_search_time:10.6f} | {cpp_search_time:10.6f}")
    print(f"{'Speedup':<20} | {'1x':<10} | {py_search_time/cpp_search_time:10.1f}x")
    print("="*30)