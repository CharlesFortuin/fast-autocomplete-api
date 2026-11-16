def calculate_edit_distance(word1: str, word2: str) -> int:
    """
    Calculates the Levenshtein (edit) distance between two words using dynamic programming.
    Returns the minimum number of edits (insertions, deletions, substitutions) to match them.
    """
    if len(word1) > len(word2):
        word1, word2 = word2, word1

    distances = range(len(word1) + 1)
    for i2, c2 in enumerate(word2):
        new_distances = [i2 + 1]
        for i1, c1 in enumerate(word1):
            if c1 == c2:
                new_distances.append(distances[i1])
            else:
                new_distances.append(1 + min((distances[i1], distances[i1 + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]


def find_spelling_suggestions(target: str, dictionary: list[str], max_distance: int = 2, top_k: int = 3) -> list[str]:
    """
    Finds words in the dictionary that are within a given edit distance 
    from the target misspelled word, sorted by closeness.
    """
    suggestions = []
    
    for word in dictionary:
        dist = calculate_edit_distance(target, word)
        if dist <= max_distance:
            suggestions.append((word, dist))
            
    # Sort primarily by edit distance (closer is better)
    suggestions.sort(key=lambda x: x[1])
    
    # Return just the top-K word strings
    return [word for word, dist in suggestions[:top_k]]