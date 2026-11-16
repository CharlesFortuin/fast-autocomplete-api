import os
import time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Query
from src.trie import Trie
from src.spellcheck import find_spelling_suggestions

app = FastAPI(
    title="Fast Autocomplete & Spell-Check API",
    description="A high-performance API powered by a custom Trie and Levenshtein distance spell-checker.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 1. Load dictionary dynamically from data/words.txt
start_time = time.perf_counter()
word_list = []
trie = Trie(top_k=5)

data_path = os.path.join("data", "words.txt")
if os.path.exists(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        lines = [line.strip().lower() for line in f if line.strip()]
        total_words = len(lines)
        for idx, word in enumerate(lines):
            if word.isalpha():
                word_list.append(word)
                rank_weight = total_words - idx
                trie.insert(word, frequency=rank_weight)

# Pre-compute the top-K cache once when the server boots up
trie.build_cache()
elapsed_ms = (time.perf_counter() - start_time) * 1000
print(f"Loaded {len(word_list):,} words and built Trie cache in {elapsed_ms:.2f} ms")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.get("/autocomplete")
def get_autocomplete(prefix: str = Query(..., min_length=1, description="The prefix string to search for")):
    suggestions = trie.search_prefix(prefix.lower())
    return {
        "query": prefix,
        "suggestions": suggestions
    }


@app.get("/spellcheck")
def get_spellcheck(
    word: str = Query(..., min_length=1, description="The target misspelled word"), 
    max_distance: int = Query(2, ge=1, le=3, description="Maximum edit distance allowed")
):
    suggestions = find_spelling_suggestions(word.lower(), word_list, max_distance=max_distance, top_k=3)
    return {
        "target": word,
        "suggestions": suggestions
    }