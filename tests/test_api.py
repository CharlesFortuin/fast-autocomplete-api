from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_serves_html_editor():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Trie & Levenshtein Live Editor" in response.text


def test_autocomplete_endpoint_returns_ranked_matches():
    response = client.get("/autocomplete", params={"prefix": "th"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "th"
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) > 0
    assert data["suggestions"][0] == "the"


def test_autocomplete_case_insensitive():
    response = client.get("/autocomplete", params={"prefix": "PY"})
    assert response.status_code == 200
    assert "python" in response.json()["suggestions"]


def test_autocomplete_empty_prefix_validation_error():
    response = client.get("/autocomplete", params={"prefix": ""})
    assert response.status_code == 422


def test_spellcheck_endpoint_corrects_typo():
    response = client.get("/spellcheck", params={"word": "algoritm", "max_distance": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["target"] == "algoritm"
    assert "algorithm" in data["suggestions"]


def test_spellcheck_invalid_max_distance_validation_error():
    # max_distance must be <= 3 per FastAPI Query constraint
    response = client.get("/spellcheck", params={"word": "test", "max_distance": 10})
    assert response.status_code == 422