import os
from fastapi import FastAPI, Query
from src.trie import Trie
from src.spellcheck import find_spelling_suggestions

app = FastAPI(
    title="Fast Autocomplete & Spell-Check API",
    description="A high-performance API powered by a custom Trie and Levenshtein distance spell-checker.",
    version="1.0.0"
)

# 1. Load dictionary dynamically from data/words.txt
word_list = []
trie = Trie(top_k=5)

data_path = os.path.join("data", "words.txt")
if os.path.exists(data_path):
    with open(data_path, "r") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                word_list.append(word)
                # Give default frequency if not specified, or parse it
                trie.insert(word, frequency=100)

# Pre-compute the top-K cache once when the server boots up
trie.build_cache()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Fast Autocomplete & Spell-Check API!"}


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