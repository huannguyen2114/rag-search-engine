# Movie Search CLI

A production-oriented movie keyword search engine with:
- BM25 ranking
- deterministic ordering
- token normalization (lowercase, punctuation removal, stopword filtering, Porter stemming)
- first-class inverted index commands

## Architecture

Project package: `movie_search`

- `movie_search/domain`: core models, tokenization, exceptions
- `movie_search/infra`: JSON and stopword repositories, cache persistence
- `movie_search/search`: BM25 and inverted index engines
- `movie_search/application`: search/index services and contracts
- `movie_search/cli.py`: CLI entrypoint

## Requirements

- Python `>=3.13`
- `uv`

## Setup

```bash
uv sync
```

## Commands

Search with BM25:

```bash
PYTHONPATH=. uv run python -m movie_search.cli search "matrix"
```

Search with JSON output:

```bash
PYTHONPATH=. uv run python -m movie_search.cli search "matrix" --limit 5 --format json
```

Build inverted index cache:

```bash
PYTHONPATH=. uv run python -m movie_search.cli index build
```

Lookup a term in the cached index:

```bash
PYTHONPATH=. uv run python -m movie_search.cli index lookup "matrix"
```

Show cached index stats:

```bash
PYTHONPATH=. uv run python -m movie_search.cli index stats
```

Using installed script entrypoint:

```bash
uv run movie-search search "matrix"
```

## Quality Gates

Run tests:

```bash
PYTHONPATH=. uv run pytest
```

Run coverage:

```bash
PYTHONPATH=. uv run pytest --cov=movie_search --cov-report=term-missing
```

Run lint:

```bash
PYTHONPATH=. uv run ruff check .
PYTHONPATH=. uv run ruff format --check .
```

Run type checking:

```bash
PYTHONPATH=. uv run mypy
```

## Data Contracts

- `data/movies.json` must contain `{"movies": [...]}`
- each movie object maps to `Movie(id, title, description)`
- non-dict movie entries are ignored
- missing `data/stopwords.txt` is treated as empty stopword set

## Error Behavior

- malformed or inaccessible movie payloads return CLI exit code `1`
- missing or invalid index cache for `index lookup`/`index stats` returns CLI exit code `1`
- no matches returns exit code `0` with user-facing message
