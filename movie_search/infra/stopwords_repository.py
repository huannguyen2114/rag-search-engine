from pathlib import Path

from movie_search.domain.exceptions import DataAccessError


class StopwordsRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load_stopwords(self) -> set[str]:
        if not self._path.exists():
            return set()
        try:
            with self._path.open("r", encoding="utf-8") as file:
                return {line.strip().lower() for line in file if line.strip()}
        except OSError as exc:
            raise DataAccessError(f"Unable to read stopwords file: {self._path}") from exc
