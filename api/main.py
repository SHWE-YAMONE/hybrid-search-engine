import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import fast_search  # Your C++ module
from preprocessing.preprocess import clean_text

app = FastAPI(title="Hybrid C++ Search Engine")

# Initialize the C++ Engine
engine = fast_search.SearchEngine()

# In-memory store for original text
doc_store: Dict[int, str] = {}

class Document(BaseModel):
    id: int
    content: str

def generate_snippet(content: str, query_tokens: List[str], window: int = 100) -> str:
    """Generates a contextual snippet with HTML highlighting."""
    if not content:
        return ""
        
    content_lower = content.lower()
    first_match_idx = -1
    
    # Use the first token that actually appears in the text
    for token in query_tokens:
        idx = content_lower.find(token.lower())
        if idx != -1:
            first_match_idx = idx
            break
            
    if first_match_idx == -1:
        return content[:window] + "..."

    # Center the window around the first match
    start = max(0, first_match_idx - (window // 2))
    end = min(len(content), first_match_idx + (window // 2))
    
    snippet = content[start:end]
    
    # Apply HTML bold tags to all query tokens
    for token in query_tokens:
        # \g<0> preserves the original casing of the matched word
        pattern = re.compile(re.escape(token), re.IGNORECASE)
        snippet = pattern.sub(f"<b>\g<0></b>", snippet)
        
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(content) else ""
    return f"{prefix}{snippet}{suffix}"

@app.post("/index")
async def index_doc(doc: Document):
    # 1. Clean and Stem text (C++ needs the exact same tokens as the search query)
    tokens = clean_text(doc.content)
    
    if not tokens:
        return {"status": "skipped", "reason": "no valid tokens"}

    # 2. Store original text for the UI/Snippets
    doc_store[int(doc.id)] = doc.content
    
    # 3. Add to C++ Inverted Index
    engine.index_document(int(doc.id), tokens)
    
    return {"status": "success", "doc_id": doc.id, "tokens_indexed": len(tokens)}

@app.get("/search")
async def search(q: str):
    # 1. Preprocess the search query (Apply same stemming as indexing)
    query_tokens = clean_text(q)
    
    if not query_tokens:
        return []

    # 2. Get ranked results from C++ Engine
    # Returns list of tuples: [(doc_id, score), ...]
    raw_results = engine.search(query_tokens)

    # 3. Enrich with snippets from Python store
    results = []
    for rid, score in raw_results:
        original_text = doc_store.get(int(rid), "")
        results.append({
            "doc_id": rid,
            "score": round(score, 4),
            "snippet": generate_snippet(original_text, query_tokens)
        })
    
    return results

@app.get("/debug")
async def get_debug_info():
    """Helper to check if data is actually in the system."""
    return {
        "indexed_docs_count": len(doc_store),
        "doc_ids": list(doc_store.keys())[:10]
    }

# Serve the Frontend UI
@app.get("/")
async def serve_ui():
    # Assumes your file is at api/static/index.html
    return FileResponse(os.path.join("api", "static", "index.html"))