#!/usr/bin/env python3

import argparse

from cli.lib.keyword_search import search_by_keyword


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search for keywords using BM25")
    search_parser.add_argument("query", help="Keyword query to search for")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for '{args.query}' using BM25")

            results = search_by_keyword(args.query)

            if not results:
                print("No results found.")
                return

            for movie in results:
                print(f"{movie.id}: {movie.title}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
