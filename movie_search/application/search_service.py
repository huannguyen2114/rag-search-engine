from movie_search.application.contracts import MovieRepository, StopwordsProvider, Tokenizer
from movie_search.domain.models import Movie
from movie_search.domain.tokenization import tokenize
from movie_search.search.bm25 import BM25SearchEngine


class SearchService:
    def __init__(
        self,
        movie_repository: MovieRepository,
        stopwords_repository: StopwordsProvider,
        tokenizer: Tokenizer = tokenize,
        engine: BM25SearchEngine | None = None,
    ) -> None:
        self._movie_repository = movie_repository
        self._stopwords_repository = stopwords_repository
        self._tokenizer = tokenizer
        self._engine = engine or BM25SearchEngine()

    def search(self, query: str, limit: int = 5) -> list[Movie]:
        if limit <= 0:
            return []

        movies = self._movie_repository.load_movies()
        stopwords = self._stopwords_repository.load_stopwords()
        query_tokens = self._tokenizer(query, stopwords)

        if not query_tokens:
            if query.strip() == "":
                return movies[:limit]
            return []

        corpus_tokens = [
            self._tokenizer(f"{movie.title} {movie.description}", stopwords) for movie in movies
        ]
        ranked = self._engine.rank(
            movies=movies,
            corpus_tokens=corpus_tokens,
            query_tokens=query_tokens,
            limit=limit,
        )
        return [item.movie for item in ranked]
