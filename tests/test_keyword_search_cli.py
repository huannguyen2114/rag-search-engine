import json

from movie_search import cli
from movie_search.domain.exceptions import DataAccessError
from movie_search.domain.models import Movie


class StubSearchService:
    def __init__(self, movies: list[Movie]) -> None:
        self._movies = movies

    def search(self, query: str, limit: int = 5) -> list[Movie]:
        return self._movies[:limit]


class StubIndexService:
    def __init__(self, lookup_result: list[int] | None = None) -> None:
        self.lookup_result = lookup_result or []
        self._stats = {"document_count": 3, "token_count": 10}
        self.loaded = False
        self.saved = False
        self.built = False

    def build(self) -> None:
        self.built = True

    def save(self) -> None:
        self.saved = True

    def load(self) -> None:
        self.loaded = True

    def lookup(self, term: str) -> list[int]:
        return self.lookup_result

    def stats(self) -> dict[str, int]:
        return self._stats


def test_search_text_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        cli,
        "create_search_service",
        lambda: StubSearchService([Movie(1, "Test Movie", "Desc")]),
    )

    exit_code = cli.main(["search", "test"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "1: Test Movie" in out


def test_search_json_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        cli,
        "create_search_service",
        lambda: StubSearchService([Movie(2, "Json Movie", "Desc")]),
    )

    exit_code = cli.main(["search", "test", "--format", "json"])
    out = capsys.readouterr().out.strip()

    assert exit_code == 0
    payload = json.loads(out)
    assert payload == [{"id": 2, "title": "Json Movie", "description": "Desc"}]


def test_search_no_results(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "create_search_service", lambda: StubSearchService([]))

    exit_code = cli.main(["search", "none"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "No results found." in out


def test_index_build(monkeypatch, capsys) -> None:
    stub = StubIndexService()
    monkeypatch.setattr(cli, "create_index_service", lambda: stub)

    exit_code = cli.main(["index", "build"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert stub.built is True
    assert stub.saved is True
    assert "Indexed 3 documents across 10 tokens." in out


def test_index_lookup_text(monkeypatch, capsys) -> None:
    stub = StubIndexService(lookup_result=[1, 2])
    monkeypatch.setattr(cli, "create_index_service", lambda: stub)

    exit_code = cli.main(["index", "lookup", "matrix"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert stub.loaded is True
    assert "1" in out and "2" in out


def test_index_lookup_json(monkeypatch, capsys) -> None:
    stub = StubIndexService(lookup_result=[3])
    monkeypatch.setattr(cli, "create_index_service", lambda: stub)

    exit_code = cli.main(["index", "lookup", "matrix", "--format", "json"])
    out = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert json.loads(out) == [3]


def test_index_stats_text(monkeypatch, capsys) -> None:
    stub = StubIndexService()
    monkeypatch.setattr(cli, "create_index_service", lambda: stub)

    exit_code = cli.main(["index", "stats"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "Documents: 3" in out
    assert "Tokens: 10" in out


def test_index_stats_json(monkeypatch, capsys) -> None:
    stub = StubIndexService()
    monkeypatch.setattr(cli, "create_index_service", lambda: stub)

    exit_code = cli.main(["index", "stats", "--format", "json"])
    out = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert json.loads(out) == {"document_count": 3, "token_count": 10}


def test_main_returns_non_zero_for_domain_errors(monkeypatch, capsys) -> None:
    def failing_service() -> StubSearchService:
        raise DataAccessError("boom")

    monkeypatch.setattr(cli, "create_search_service", failing_service)

    exit_code = cli.main(["search", "test"])
    err = capsys.readouterr().err

    assert exit_code == 1
    assert "Error: boom" in err
