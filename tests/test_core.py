from src.trie import Trie
from src.spellcheck import find_spelling_suggestions


def test_trie_frequency_ranking_and_top_k():
    trie = Trie(top_k=3)
    trie.insert("python", frequency=500)
    trie.insert("pytorch", frequency=300)
    trie.insert("pytest", frequency=400)
    trie.insert("pygame", frequency=100)
    trie.build_cache()

    results = trie.search_prefix("py")
    assert results == ["python", "pytest", "pytorch"]


def test_trie_alphabetical_tie_breaking():
    trie = Trie(top_k=3)
    trie.insert("cat", frequency=100)
    trie.insert("car", frequency=100)
    trie.insert("cab", frequency=100)
    trie.build_cache()

    results = trie.search_prefix("ca")
    assert results == ["cab", "car", "cat"]


def test_trie_unknown_prefix_returns_empty():
    trie = Trie(top_k=5)
    trie.insert("apple", frequency=100)
    trie.build_cache()

    assert trie.search_prefix("xyz") == []


def test_spellcheck_edit_distance_ranking():
    dictionary = ["python", "cython", "typhon", "fastapi", "javascript"]
    
    # "pyton" is 1 edit away from "python"
    suggestions = find_spelling_suggestions("pyton", dictionary, max_distance=2, top_k=2)
    assert suggestions[0] == "python"


def test_spellcheck_respects_max_distance():
    dictionary = ["python", "fastapi"]
    
    # "zzzzzz" has edit distance > 2 from all words
    suggestions = find_spelling_suggestions("zzzzzz", dictionary, max_distance=2, top_k=3)
    assert suggestions == []