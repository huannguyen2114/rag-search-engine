import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from movie_search.domain.exceptions import IndexStoreError


@dataclass(frozen=True, slots=True)
class StoredIndex:
    index: dict[str, list[int]]
    docmap: dict[int, str]


class PickleIndexStore:
    def __init__(
        self,
        cache_dir: Path,
        index_filename: str = "index.pkl",
        docmap_filename: str = "docmap.pkl",
    ) -> None:
        self._cache_dir = cache_dir
        self._index_path = cache_dir / index_filename
        self._docmap_path = cache_dir / docmap_filename

    def save(self, index: dict[str, set[int]], docmap: dict[int, str]) -> None:
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        normalized_index = {
            token: sorted(doc_ids)
            for token, doc_ids in sorted(index.items(), key=lambda item: item[0])
        }
        normalized_docmap = dict(sorted(docmap.items(), key=lambda item: item[0]))

        try:
            with self._index_path.open("wb") as index_file:
                pickle.dump(normalized_index, index_file, protocol=pickle.HIGHEST_PROTOCOL)
            with self._docmap_path.open("wb") as docmap_file:
                pickle.dump(normalized_docmap, docmap_file, protocol=pickle.HIGHEST_PROTOCOL)
        except (OSError, pickle.PickleError) as exc:
            raise IndexStoreError(f"Unable to persist index cache at {self._cache_dir}") from exc

    def load(self) -> StoredIndex:
        try:
            with self._index_path.open("rb") as index_file:
                raw_index = pickle.load(index_file)
            with self._docmap_path.open("rb") as docmap_file:
                raw_docmap = pickle.load(docmap_file)
        except FileNotFoundError as exc:
            raise IndexStoreError(f"Index cache not found in {self._cache_dir}") from exc
        except (OSError, pickle.PickleError) as exc:
            raise IndexStoreError(f"Unable to load index cache from {self._cache_dir}") from exc

        return StoredIndex(
            index=self._validate_index(raw_index),
            docmap=self._validate_docmap(raw_docmap),
        )

    def _validate_index(self, value: Any) -> dict[str, list[int]]:
        if not isinstance(value, dict):
            raise IndexStoreError("Cached index payload must be a dictionary.")
        validated: dict[str, list[int]] = {}
        for token, doc_ids in value.items():
            if not isinstance(token, str):
                raise IndexStoreError("Cached index token keys must be strings.")
            if not isinstance(doc_ids, list) or not all(
                isinstance(doc_id, int) for doc_id in doc_ids
            ):
                raise IndexStoreError("Cached index values must be lists of document IDs.")
            validated[token] = sorted(set(doc_ids))
        return validated

    def _validate_docmap(self, value: Any) -> dict[int, str]:
        if not isinstance(value, dict):
            raise IndexStoreError("Cached docmap payload must be a dictionary.")
        validated: dict[int, str] = {}
        for doc_id, content in value.items():
            if not isinstance(doc_id, int):
                raise IndexStoreError("Cached docmap keys must be integer document IDs.")
            if not isinstance(content, str):
                raise IndexStoreError("Cached docmap values must be strings.")
            validated[doc_id] = content
        return dict(sorted(validated.items(), key=lambda item: item[0]))
