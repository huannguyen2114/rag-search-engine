from movie_search.domain.models import Movie


def test_movie_from_mapping_success() -> None:
    data = {
        "id": 1,
        "title": "Inception",
        "description": "Dream heist",
    }
    movie = Movie.from_mapping(data)
    assert movie.id == 1
    assert movie.title == "Inception"
    assert movie.description == "Dream heist"


def test_movie_from_mapping_partial_data() -> None:
    movie = Movie.from_mapping({"id": 2, "title": "The Matrix"})
    assert movie.id == 2
    assert movie.title == "The Matrix"
    assert movie.description == ""


def test_movie_to_dict() -> None:
    movie = Movie(id=3, title="Interstellar", description="Space")
    assert movie.to_dict() == {
        "id": 3,
        "title": "Interstellar",
        "description": "Space",
    }
