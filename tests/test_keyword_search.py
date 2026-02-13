from movie_search.application.search_service import SearchService
from movie_search.domain.models import Movie


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


def _service(movies: list[Movie], stopwords: set[str] | None = None) -> SearchService:
    return SearchService(
        movie_repository=StubMovieRepository(movies),
        stopwords_repository=StubStopwordsRepository(stopwords or {"the", "and", "a"}),
    )


def test_search_found() -> None:
    service = _service(
        [
            Movie(1, "The Matrix", "Sci-fi"),
            Movie(2, "Inception", "Dream heist"),
            Movie(3, "The Matrix Reloaded", "Sci-fi sequel"),
        ]
    )

    results = service.search("Matrix")
    assert len(results) == 2
    assert results[0].title == "The Matrix"
    assert results[1].title == "The Matrix Reloaded"


def test_search_case_insensitive() -> None:
    service = _service([Movie(1, "The Matrix", "Sci-fi")])
    results = service.search("matrix")
    assert len(results) == 1
    assert results[0].title == "The Matrix"


def test_search_punctuation_behavior() -> None:
    service = _service([Movie(1, "Spider-Man", "Marvel movie")])

    results = service.search("SpiderMan")
    assert len(results) == 1
    assert results[0].title == "Spider-Man"

    results = service.search("Spider-Man")
    assert len(results) == 1


def test_search_limit() -> None:
    service = _service([Movie(i, f"Movie {i}", "Desc") for i in range(10)])
    results = service.search("Movie", limit=3)
    assert len(results) == 3


def test_search_no_match() -> None:
    service = _service([Movie(1, "The Matrix", "Sci-fi")])
    assert service.search("Inception") == []


def test_search_empty_query_returns_first_n() -> None:
    service = _service([Movie(1, "The Matrix", "Sci-fi"), Movie(2, "Inception", "Dream heist")])
    results = service.search("", limit=1)
    assert len(results) == 1
    assert results[0].id == 1


def test_search_by_token() -> None:
    service = _service([Movie(1, "Big Bear", "A Big Bear")])
    results = service.search("Small Bear")
    assert len(results) == 1


def test_search_ranking() -> None:
    service = _service(
        [
            Movie(1, "The Matrix", "Sci-fi action movie with simulation"),
            Movie(2, "Matrix Reloaded", "Second Matrix movie"),
            Movie(3, "Simulation", "A movie about simulation"),
        ]
    )

    results = service.search("simulation")
    assert len(results) == 2
    assert results[0].id == 3
    assert results[1].id == 1

    results = service.search("Matrix")
    assert len(results) == 2
    assert results[0].id == 2
    assert results[1].id == 1


def test_search_all_stopwords() -> None:
    service = _service([Movie(1, "The Matrix", "Sci-fi")])
    assert service.search("the") == []


def test_search_only_punctuation() -> None:
    service = _service([Movie(1, "The Matrix", "Sci-fi")])
    assert service.search("!!!") == []


def test_search_non_positive_limit() -> None:
    service = _service([Movie(1, "The Matrix", "Sci-fi")])
    assert service.search("Matrix", limit=0) == []
