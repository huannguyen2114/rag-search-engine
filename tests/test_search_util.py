import json
from pathlib import Path

import pytest

from movie_search.domain.exceptions import DataAccessError, DataFormatError
from movie_search.infra.json_repository import JsonMovieRepository
from movie_search.infra.stopwords_repository import StopwordsRepository


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_load_movies_success(tmp_path: Path) -> None:
    movies_path = tmp_path / "movies.json"
    _write_text(
        movies_path,
        json.dumps({"movies": [{"id": 1, "title": "Test", "description": "Desc"}]}),
    )

    repository = JsonMovieRepository(movies_path)
    movies = repository.load_movies()

    assert len(movies) == 1
    assert movies[0].id == 1
    assert movies[0].title == "Test"


def test_load_movies_invalid_movies_type(tmp_path: Path) -> None:
    movies_path = tmp_path / "movies.json"
    _write_text(movies_path, json.dumps({"movies": "bad"}))

    repository = JsonMovieRepository(movies_path)
    with pytest.raises(DataFormatError):
        repository.load_movies()


def test_load_movies_missing_movies_key(tmp_path: Path) -> None:
    movies_path = tmp_path / "movies.json"
    _write_text(movies_path, json.dumps({"other": []}))

    repository = JsonMovieRepository(movies_path)
    assert repository.load_movies() == []


def test_load_movies_filters_non_dict_items(tmp_path: Path) -> None:
    movies_path = tmp_path / "movies.json"
    _write_text(
        movies_path,
        json.dumps({"movies": [{"id": 1, "title": "Test"}, "invalid", 1]}),
    )

    repository = JsonMovieRepository(movies_path)
    movies = repository.load_movies()
    assert len(movies) == 1
    assert movies[0].id == 1


def test_load_movies_missing_file_raises(tmp_path: Path) -> None:
    repository = JsonMovieRepository(tmp_path / "missing.json")
    with pytest.raises(DataAccessError):
        repository.load_movies()


def test_load_movies_malformed_json_raises(tmp_path: Path) -> None:
    movies_path = tmp_path / "movies.json"
    _write_text(movies_path, "{bad json")

    repository = JsonMovieRepository(movies_path)
    with pytest.raises(DataFormatError):
        repository.load_movies()


def test_load_stopwords_success(tmp_path: Path) -> None:
    stopwords_path = tmp_path / "stopwords.txt"
    _write_text(stopwords_path, "the\nAND\n")

    repository = StopwordsRepository(stopwords_path)
    assert repository.load_stopwords() == {"the", "and"}


def test_load_stopwords_missing_file_returns_empty_set(tmp_path: Path) -> None:
    repository = StopwordsRepository(tmp_path / "missing.txt")
    assert repository.load_stopwords() == set()
