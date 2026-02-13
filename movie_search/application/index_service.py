from movie_search.application.contracts import (
    IndexStore,
    MovieRepository,
    StopwordsProvider,
    Tokenizer,
)
from movie_search.domain.tokenization import tokenize
from movie_search.search.inverted_index import InvertedIndex


class IndexService:
    def __init__(
        self,
        movie_repository: MovieRepository,
        stopwords_repository: StopwordsProvider,
        index_store: IndexStore,
        tokenizer: Tokenizer = tokenize,
        index: InvertedIndex | None = None,
    ) -> None:
        self._movie_repository = movie_repository
        self._stopwords_repository = stopwords_repository
        self._index_store = index_store
        self._tokenizer = tokenizer
        self._index = index or InvertedIndex()

    def build(self) -> None:
        movies = self._movie_repository.load_movies()
        stopwords = self._stopwords_repository.load_stopwords()
        self._index.build(movies=movies, stopwords=stopwords, tokenizer=self._tokenizer)

    def lookup(self, term: str) -> list[int]:
        stopwords = self._stopwords_repository.load_stopwords()
        term_tokens = self._tokenizer(term, stopwords)
        return self._index.lookup(term_tokens)

    def save(self) -> None:
        self._index_store.save(index=self._index.export_index(), docmap=self._index.export_docmap())

    def load(self) -> None:
        stored = self._index_store.load()
        self._index.import_data(index=stored.index, docmap=stored.docmap)

    def stats(self) -> dict[str, int]:
        return self._index.stats()
