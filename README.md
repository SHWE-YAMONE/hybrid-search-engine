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

## Architected for Production
Instead of building a simple "script," I designed this as a production-ready system:

Containerized: The entire system is portable; a single docker build command compiles the C++ and sets up the environment.

Scalable: The separation of the Crawler (I/O heavy) and the Engine (CPU heavy) allows them to scale independently.

Test-Driven: Includes a suite of integration tests to ensure that the memory-safe C++ core communicates perfectly with the Python wrapper.
