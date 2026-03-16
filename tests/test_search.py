import pytest
import fast_search
from preprocessing.preprocess import clean_text

@pytest.fixture
def engine():
    """Initializes a fresh C++ engine for each test."""
    return fast_search.SearchEngine()

def test_basic_indexing_and_search(engine):
    """Check if the engine can find a word in a single document."""
    doc_id = 1
    content = "The quick brown fox jumps over the lazy dog"
    tokens = clean_text(content)
    
    engine.index_document(doc_id, tokens)
    results = engine.search(["fox"])
    
    assert len(results) == 1
    assert results[0][0] == doc_id
    assert results[0][1] > 0  # Score should be positive

def test_ranking_relevance(engine):
    """Verify that a document with higher term frequency ranks higher."""
    # Doc 1 has 'apple' once
    engine.index_document(1, ["apple", "banana"])
    # Doc 2 has 'apple' twice (more relevant)
    engine.index_document(2, ["apple", "apple", "orange"])
    
    results = engine.search(["apple"])
    
    assert len(results) == 2
    assert results[0][0] == 2  # Doc 2 should be ranked #1
    assert results[0][1] > results[1][1]

def test_empty_query(engine):
    """Ensure the engine handles empty input gracefully without crashing."""
    engine.index_document(1, ["test"])
    results = engine.search([])
    assert results == []

def test_stopword_filtering():
    """Validate that our preprocessing correctly filters noise."""
    text = "This is a test"
    tokens = clean_text(text)
    # Depending on your stopword list, 'is' and 'a' should be gone
    assert "is" not in tokens
    assert "test" in tokens

def test_multi_word_query(engine):
    """Check if the engine calculates combined scores for multiple terms."""
    engine.index_document(1, ["python", "cpp"])
    engine.index_document(2, ["python", "java"])
    
    # Searching for 'python' and 'cpp'
    results = engine.search(["python", "cpp"])
    
    # Doc 1 should rank higher because it matches both terms
    assert results[0][0] == 1