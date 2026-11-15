from src.trie import Trie

# 1. Initialize Trie and set top_k to 3
trie = Trie(top_k=3)

# 2. Insert some test words with different frequencies
words_to_insert = [
    ("python", 500),
    ("pycharm", 200),
    ("pygame", 150),
    ("pypi", 300),
    ("performance", 400)
]

for word, freq in words_to_insert:
    trie.insert(word, freq)

# 3. Build the cache so top_suggestions are populated
trie.build_cache()

# 4. Test prefix searches
print("Prefix 'py':", trie.search_prefix("py"))
print("Prefix 'per':", trie.search_prefix("per"))
print("Prefix 'xyz':", trie.search_prefix("xyz"))