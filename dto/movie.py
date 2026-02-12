from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MovieDTO:
    id: int
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'MovieDTO':
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")

        movie_id = data.get("id", 0)
        title = data.get("title", "")
        description = data.get("description", "")

        return cls(movie_id, title, description)
