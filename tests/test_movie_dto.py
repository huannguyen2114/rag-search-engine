from unittest import TestCase

from dto.movie import MovieDTO


class TestMovieDTO(TestCase):

    def test_from_dict_success(self):
        data = {
            "id": 1,
            "title": "Inception",
            "description": "A thief who steals corporate secrets through the use of dream-sharing technology."
        }
        movie = MovieDTO.from_dict(data)
        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.description,
                         "A thief who steals corporate secrets through the use of dream-sharing technology.")

    def test_from_dict_partial_data(self):
        data = {"id": 2, "title": "The Matrix"}
        movie = MovieDTO.from_dict(data)
        self.assertEqual(movie.id, 2)
        self.assertEqual(movie.title, "The Matrix")
        self.assertEqual(movie.description, "")

    def test_from_dict_empty_dict(self):
        movie = MovieDTO.from_dict({})
        self.assertEqual(movie.id, 0)
        self.assertEqual(movie.title, "")
        self.assertEqual(movie.description, "")

    def test_from_dict_invalid_type(self):
        with self.assertRaises(ValueError) as cm:
            MovieDTO.from_dict(["not", "a", "dict"])
        self.assertIn("Expected dict", str(cm.exception))
