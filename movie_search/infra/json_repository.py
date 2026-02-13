import json
from pathlib import Path
from typing import Any

from movie_search.domain.exceptions import DataAccessError, DataFormatError
from movie_search.domain.models import Movie


class JsonMovieRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load_movies(self) -> list[Movie]:
        payload = self._read_payload()
        movies_raw = payload.get("movies", [])
        if not isinstance(movies_raw, list):
            raise DataFormatError(
                f"Expected 'movies' to be a list, got {type(movies_raw).__name__}."
            )
        return [Movie.from_mapping(item) for item in movies_raw if isinstance(item, dict)]

    def _read_payload(self) -> dict[str, Any]:
        try:
            with self._path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError as exc:
            raise DataAccessError(f"Movies file not found: {self._path}") from exc
        except OSError as exc:
            raise DataAccessError(f"Unable to read movies file: {self._path}") from exc
        except json.JSONDecodeError as exc:
            raise DataFormatError(f"Malformed JSON in movies file: {self._path}") from exc

        if not isinstance(payload, dict):
            raise DataFormatError(
                f"Expected movies payload to be an object, got {type(payload).__name__}."
            )
        return payload
