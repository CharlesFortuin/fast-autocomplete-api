class TrieNode:
    def __init__(self):
        self.children ={}
        self.is_end = False
        self.frequency = 0
        self.top_suggestions: list[tuple[str, int]] = []

class Trie:
    def __init__(self, top_k: int = 5):
        self.root = TrieNode()
        self.top_k = top_k

    def insert(self, word: str, frequency: int) -> None:
        """Inserts a word and its frequency into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end = True
        node.frequency = frequency

    def build_cache(self) -> None:
        """
        Recursively computes and stores the top-K suggestions at every node.
        This trades a bit of memory for sub-millisecond O(1) query lookups later.
        """
        def _dfs(node: TrieNode) -> list[tuple[str, int]]:
            results = []
            if node.is_end:
                results.append(("", node.frequency))
            
            for char, child in node.children.items():
                for sub_word, freq in _dfs(child):
                    results.append((char + sub_word, freq))
            
            # Sort descending by frequency, then slice top K
            results.sort(key=lambda x: x[1], reverse=True)
            node.top_suggestions = results[:self.top_k]
            return results

        _dfs(self.root)

    def search_prefix(self, prefix: str) -> list[str]:
        """
        Finds the top-K autocomplete suggestions for a given prefix.
        Runs in O(L) time where L is the length of the prefix.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Immediate retrieval using the pre-computed cache
        return [prefix + word for word, _ in node.top_suggestions]