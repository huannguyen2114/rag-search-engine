from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Movie:
    id: int
    title: str
    description: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Movie":
        movie_id = data.get("id", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        return cls(int(movie_id), str(title), str(description))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class SearchResult:
    movie: Movie
    score: float
