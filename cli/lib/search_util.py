import json
from pathlib import Path

from dto.movie import MovieDTO

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "movies.json"


def load_movies() -> list[MovieDTO]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    movies = payload.get("movies", [])
    if not isinstance(movies, list):
        raise ValueError(f"Expected 'movies' key in payload to be a list, got {type(movies)}")
    return [MovieDTO.from_dict(item) for item in movies if isinstance(item, dict)]
