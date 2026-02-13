from pathlib import Path

import pytest

from movie_search.domain.exceptions import IndexStoreError
from movie_search.infra.index_store import PickleIndexStore


def test_index_store_save_and_load_roundtrip(tmp_path: Path) -> None:
    store = PickleIndexStore(tmp_path)
    index = {"matrix": {2, 1}, "action": {1}}
    docmap = {2: "Matrix Reloaded", 1: "The Matrix"}

    store.save(index=index, docmap=docmap)
    stored = store.load()

    assert stored.index == {"action": [1], "matrix": [1, 2]}
    assert stored.docmap == {1: "The Matrix", 2: "Matrix Reloaded"}


def test_index_store_load_missing_cache_raises(tmp_path: Path) -> None:
    store = PickleIndexStore(tmp_path)
    with pytest.raises(IndexStoreError):
        store.load()


def test_index_store_rejects_invalid_payload(tmp_path: Path) -> None:
    store = PickleIndexStore(tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "index.pkl").write_bytes(b"not a pickle")
    (tmp_path / "docmap.pkl").write_bytes(b"not a pickle")

    with pytest.raises(IndexStoreError):
        store.load()
