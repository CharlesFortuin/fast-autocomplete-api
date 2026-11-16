from src.spellcheck import find_spelling_suggestions

word_list = ["python", "pycharm", "pygame", "pypi", "performance", "apple"]

typo = "pyton"
suggestions = find_spelling_suggestions(typo, word_list, max_distance=2, top_k=3)

print(f"Suggestions for typo '{typo}':", suggestions)