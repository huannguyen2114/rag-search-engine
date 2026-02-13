from collections.abc import Callable
from typing import Protocol

from movie_search.domain.models import Movie
from movie_search.infra.index_store import StoredIndex

Tokenizer = Callable[[str, set[str]], list[str]]


class MovieRepository(Protocol):
    def load_movies(self) -> list[Movie]: ...


class StopwordsProvider(Protocol):
    def load_stopwords(self) -> set[str]: ...


class IndexStore(Protocol):
    def save(self, index: dict[str, set[int]], docmap: dict[int, str]) -> None: ...

    def load(self) -> StoredIndex: ...
