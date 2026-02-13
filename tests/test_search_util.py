from unittest import TestCase
from unittest.mock import patch, mock_open

from cli.lib.search_util import load_movies


class TestSearchUtil(TestCase):

    @patch("pathlib.Path.open", new_callable=mock_open,
           read_data='{"movies": [{"id": 1, "title": "Test", "description": "Desc"}]}')
    def test_load_movies_success(self, mock_file):
        movies = load_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].id, 1)
        self.assertEqual(movies[0].title, "Test")

    @patch("pathlib.Path.open", new_callable=mock_open, read_data='{"movies": "not a list"}')
    def test_load_movies_invalid_format(self, mock_file):
        with self.assertRaises(ValueError) as cm:
            load_movies()
        self.assertIn("Expected 'movies' key in payload to be a list", str(cm.exception))

    @patch("pathlib.Path.open", new_callable=mock_open, read_data='{"other": []}')
    def test_load_movies_missing_key(self, mock_file):
        # payload.get("movies", []) returns [], so it should return empty list of movies
        movies = load_movies()
        self.assertEqual(len(movies), 0)

    @patch("pathlib.Path.open", new_callable=mock_open, read_data='{"movies": [{"id": 1, "title": "Test"}, "invalid"]}')
    def test_load_movies_filters_invalid_items(self, mock_file):
        # It should skip "invalid" because it's not a dict
        movies = load_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].id, 1)
