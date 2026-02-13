from pathlib import Path

from movie_search.application.index_service import IndexService
from movie_search.domain.models import Movie
from movie_search.infra.index_store import PickleIndexStore


class StubMovieRepository:
    def __init__(self, movies: list[Movie]) -> None:
        self._movies = movies

    def load_movies(self) -> list[Movie]:
        return self._movies


class StubStopwordsRepository:
    def __init__(self, stopwords: set[str]) -> None:
        self._stopwords = stopwords

    def load_stopwords(self) -> set[str]:
        return self._stopwords


def test_index_service_build_lookup_save_load(tmp_path: Path) -> None:
    movies = [
        Movie(1, "The Matrix", "Action sci-fi"),
        Movie(2, "Inception", "Dream action"),
    ]
    movie_repo = StubMovieRepository(movies)
    stopwords_repo = StubStopwordsRepository({"the"})
    store = PickleIndexStore(tmp_path)

    service = IndexService(
        movie_repository=movie_repo, stopwords_repository=stopwords_repo, index_store=store
    )
    service.build()

    assert service.lookup("matrix") == [1]

    service.save()
    restored = IndexService(
        movie_repository=movie_repo, stopwords_repository=stopwords_repo, index_store=store
    )
    restored.load()

    assert restored.lookup("action") == [1, 2]
    stats = restored.stats()
    assert stats["document_count"] == 2
    assert stats["token_count"] > 0
