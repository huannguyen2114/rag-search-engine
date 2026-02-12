import argparse
from unittest import TestCase
from unittest.mock import patch

from cli.keyword_search_cli import main


class TestKeywordSearchCLI(TestCase):

    @patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(command="search", query="test"))
    @patch("builtins.print")
    def test_main_search_command(self, mock_print, mock_args):
        """ Test when the 'search' command is provided with a query. """
        main()
        mock_print.assert_called_with("Searching for 'test' using BM25")

    @patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(command=None))
    @patch("argparse.ArgumentParser.print_help")
    def test_main_no_command(self, mock_print_help, mock_args):
        """ Test when no command is provided. """
        main()
        mock_print_help.assert_called_once()
