# AGENTS.md

This guide defines how humans and coding agents should contribute to this repository.

## Project Purpose
- Build and maintain a movie keyword search engine.
- Expose production-ready search and index workflows through a CLI.
- Keep behavior deterministic and test-covered.

## Tech Stack
- Python `>=3.13` (managed with `uv`)
- `pytest` + `pytest-cov` for tests and coverage
- `ruff` for lint/format checks
- `mypy` for static typing checks
- `nltk` (`PorterStemmer`) for token normalization

## Repository Layout
- `movie_search/domain/models.py`: core data models.
- `movie_search/domain/tokenization.py`: normalization logic.
- `movie_search/domain/exceptions.py`: typed domain errors.
- `movie_search/infra/json_repository.py`: movie loading adapter.
- `movie_search/infra/stopwords_repository.py`: stopword loading adapter.
- `movie_search/infra/index_store.py`: index persistence adapter.
- `movie_search/search/bm25.py`: BM25 ranking engine.
- `movie_search/search/inverted_index.py`: inverted index engine.
- `movie_search/application/search_service.py`: search use case orchestration.
- `movie_search/application/index_service.py`: index use case orchestration.
- `movie_search/cli.py`: CLI entrypoint.
- `data/movies.json`: source corpus.
- `data/stopwords.txt`: stopword list.
- `tests/`: unit and integration tests.

## Setup And Commands
1. Install dependencies:
   - `uv sync`
2. Run search CLI:
   - `PYTHONPATH=. uv run python -m movie_search.cli search "matrix"`
3. Run index build:
   - `PYTHONPATH=. uv run python -m movie_search.cli index build`
4. Run tests:
   - `PYTHONPATH=. uv run pytest`
5. Run coverage:
   - `PYTHONPATH=. uv run pytest --cov=movie_search --cov-report=term-missing`
6. Run lint and format check:
   - `PYTHONPATH=. uv run ruff check .`
   - `PYTHONPATH=. uv run ruff format --check .`
7. Run type checking:
   - `PYTHONPATH=. uv run mypy`

## Coding Rules
- Preserve typed signatures and dataclass usage.
- Keep file I/O via `pathlib.Path` and project-root-relative paths.
- Keep tokenization behavior consistent unless intentionally changing ranking semantics:
  - lowercase
  - punctuation removal
  - stopword filtering
  - Porter stemming
- Keep search ordering deterministic (`score desc`, stable tiebreak by movie id).
- Prefer focused changes over broad unrelated rewrites.

## Testing Rules
- Any behavior change must include or update tests in `tests/`.
- Add regression tests for bug fixes.
- Keep tests independent from network or external services.
- Maintain overall coverage >= 90%.

## Data Contracts
- `data/movies.json` contains `{"movies": [...]}`.
- Each movie maps to `Movie(id, title, description)`.
- Invalid non-dict movie entries are ignored.
- Missing stopwords file returns an empty stopword set.

## Agent Workflow Checklist
1. Read affected modules and related tests first.
2. Implement minimal changes that satisfy requirements.
3. Run targeted tests, then the full suite and quality gates.
4. Update docs (`README.md`, this file) when behavior or workflow changes.
5. Summarize what changed, what was tested, and any known limitations.
