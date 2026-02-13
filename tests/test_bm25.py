from movie_search.domain.models import Movie
from movie_search.search.bm25 import BM25SearchEngine


def test_bm25_ranking_and_tiebreaker() -> None:
    engine = BM25SearchEngine()
    movies = [
        Movie(2, "Alpha", "matrix"),
        Movie(1, "Beta", "matrix"),
    ]
    corpus_tokens = [["matrix"], ["matrix"]]

    results = engine.rank(
        movies=movies, corpus_tokens=corpus_tokens, query_tokens=["matrix"], limit=5
    )

    assert [item.movie.id for item in results] == [1, 2]


def test_bm25_handles_empty_corpus_tokens() -> None:
    engine = BM25SearchEngine()
    movies = [Movie(1, "Title", "Desc")]
    corpus_tokens = [[]]

    results = engine.rank(
        movies=movies, corpus_tokens=corpus_tokens, query_tokens=["matrix"], limit=5
    )
    assert results == []
