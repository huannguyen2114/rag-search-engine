from cli.lib.search_util import load_movies
from dto.movie import MovieDTO


def search_by_keyword(query, number_of_results=5) -> list[MovieDTO]:
    movies = load_movies()
    query = (query or "").lower()

    results: list[MovieDTO] = []
    for movie in movies:
        title = movie.title
        if query in title.lower():
            results.append(movie)
        if len(results) >= number_of_results:
            break

    return results
