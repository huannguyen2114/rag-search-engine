class MovieSearchError(Exception):
    """Base exception for movie search errors."""


class DataAccessError(MovieSearchError):
    """Raised when a data source cannot be accessed."""


class DataFormatError(MovieSearchError):
    """Raised when data payloads are malformed or unexpected."""


class IndexStoreError(MovieSearchError):
    """Raised when index persistence operations fail."""
