from movie_search.domain.models import Movie
from movie_search.domain.tokenization import tokenize
from movie_search.search.inverted_index import InvertedIndex


def test_inverted_index_build_lookup_and_stats() -> None:
    index = InvertedIndex()
    movies = [
        Movie(1, "The Matrix", "Sci-fi"),
        Movie(2, "Matrix Reloaded", "Sci-fi sequel"),
    ]

    index.build(movies=movies, stopwords={"the"}, tokenizer=tokenize)

    assert index.lookup(["matrix"]) == [1, 2]
    stats = index.stats()
    assert stats["document_count"] == 2
    assert stats["token_count"] > 0


def test_inverted_index_lookup_intersection() -> None:
    index = InvertedIndex()
    movies = [
        Movie(1, "The Matrix", "Sci-fi"),
        Movie(2, "Matrix", "Drama"),
    ]
    index.build(movies=movies, stopwords={"the"}, tokenizer=tokenize)

    # Only doc 1 has both terms.
    assert index.lookup(["matrix", "scifi"]) == [1]


def test_inverted_index_export_import_roundtrip() -> None:
    index = InvertedIndex()
    movies = [Movie(10, "Matrix", "Action")]
    index.build(movies=movies, stopwords=set(), tokenizer=tokenize)

    exported_index = {token: sorted(doc_ids) for token, doc_ids in index.export_index().items()}
    exported_docmap = index.export_docmap()

    restored = InvertedIndex()
    restored.import_data(exported_index, exported_docmap)

    assert restored.lookup(["matrix"]) == [10]
