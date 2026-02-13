from collections.abc import Callable

from movie_search.domain.models import Movie


class InvertedIndex:
    def __init__(self) -> None:
        self._index: dict[str, set[int]] = {}
        self._docmap: dict[int, str] = {}

    def build(
        self,
        movies: list[Movie],
        stopwords: set[str],
        tokenizer: Callable[[str, set[str]], list[str]],
    ) -> None:
        self.clear()
        for movie in movies:
            content = f"{movie.title} {movie.description}"
            self._docmap[movie.id] = content
            for token in set(tokenizer(content, stopwords)):
                self._index.setdefault(token, set()).add(movie.id)

    def clear(self) -> None:
        self._index.clear()
        self._docmap.clear()

    def lookup(self, term_tokens: list[str]) -> list[int]:
        if not term_tokens:
            return []

        doc_ids: set[int] | None = None
        for token in term_tokens:
            token_docs = self._index.get(token, set())
            if doc_ids is None:
                doc_ids = set(token_docs)
            else:
                doc_ids &= token_docs
            if not doc_ids:
                return []

        return sorted(doc_ids) if doc_ids is not None else []

    def stats(self) -> dict[str, int]:
        return {
            "token_count": len(self._index),
            "document_count": len(self._docmap),
        }

    def export_index(self) -> dict[str, set[int]]:
        return {token: set(doc_ids) for token, doc_ids in self._index.items()}

    def export_docmap(self) -> dict[int, str]:
        return dict(self._docmap)

    def import_data(self, index: dict[str, list[int]], docmap: dict[int, str]) -> None:
        self._index = {token: set(doc_ids) for token, doc_ids in index.items()}
        self._docmap = dict(docmap)
