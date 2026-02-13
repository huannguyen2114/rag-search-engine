import argparse
import json
import sys
from collections.abc import Sequence

from movie_search.application.index_service import IndexService
from movie_search.application.search_service import SearchService
from movie_search.domain.exceptions import MovieSearchError
from movie_search.infra.index_store import PickleIndexStore
from movie_search.infra.json_repository import JsonMovieRepository
from movie_search.infra.stopwords_repository import StopwordsRepository
from movie_search.settings import CACHE_DIR, MOVIES_PATH, STOPWORDS_PATH


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Movie keyword search CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", help="Query to search")
    search_parser.add_argument(
        "--limit", type=int, default=5, help="Maximum number of movies to return"
    )
    search_parser.add_argument(
        "--format",
        dest="output_format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )

    index_parser = subparsers.add_parser("index", help="Inverted index operations")
    index_subparsers = index_parser.add_subparsers(dest="index_command", required=True)

    index_subparsers.add_parser("build", help="Build and persist the inverted index")

    lookup_parser = index_subparsers.add_parser("lookup", help="Lookup documents for a term")
    lookup_parser.add_argument("term", help="Term to look up")
    lookup_parser.add_argument(
        "--format",
        dest="output_format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )

    stats_parser = index_subparsers.add_parser("stats", help="Show index statistics")
    stats_parser.add_argument(
        "--format",
        dest="output_format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )

    return parser


def create_search_service() -> SearchService:
    movie_repo = JsonMovieRepository(MOVIES_PATH)
    stopwords_repo = StopwordsRepository(STOPWORDS_PATH)
    return SearchService(movie_repository=movie_repo, stopwords_repository=stopwords_repo)


def create_index_service() -> IndexService:
    movie_repo = JsonMovieRepository(MOVIES_PATH)
    stopwords_repo = StopwordsRepository(STOPWORDS_PATH)
    store = PickleIndexStore(CACHE_DIR)
    return IndexService(
        movie_repository=movie_repo, stopwords_repository=stopwords_repo, index_store=store
    )


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "search":
        return _run_search(args.query, args.limit, args.output_format)

    if args.command == "index":
        if args.index_command == "build":
            return _run_index_build()
        if args.index_command == "lookup":
            return _run_index_lookup(args.term, args.output_format)
        if args.index_command == "stats":
            return _run_index_stats(args.output_format)

    parser.print_help()
    return 2


def _run_search(query: str, limit: int, output_format: str) -> int:
    service = create_search_service()
    movies = service.search(query=query, limit=limit)

    if output_format == "json":
        payload = [movie.to_dict() for movie in movies]
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    if not movies:
        print("No results found.")
        return 0

    for movie in movies:
        print(f"{movie.id}: {movie.title}")
    return 0


def _run_index_build() -> int:
    service = create_index_service()
    service.build()
    service.save()
    stats = service.stats()
    print(f"Indexed {stats['document_count']} documents across {stats['token_count']} tokens.")
    return 0


def _run_index_lookup(term: str, output_format: str) -> int:
    service = create_index_service()
    service.load()
    doc_ids = service.lookup(term)

    if output_format == "json":
        print(json.dumps(doc_ids))
        return 0

    if not doc_ids:
        print("No documents found.")
        return 0

    for doc_id in doc_ids:
        print(doc_id)
    return 0


def _run_index_stats(output_format: str) -> int:
    service = create_index_service()
    service.load()
    stats = service.stats()

    if output_format == "json":
        print(json.dumps(stats))
        return 0

    print(f"Documents: {stats['document_count']}")
    print(f"Tokens: {stats['token_count']}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return run(argv=argv)
    except MovieSearchError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
