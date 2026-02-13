import math
from collections import Counter
from dataclasses import dataclass

from movie_search.domain.models import Movie, SearchResult


@dataclass(frozen=True, slots=True)
class BM25Config:
    k1: float = 1.5
    b: float = 0.75


class BM25SearchEngine:
    def __init__(self, config: BM25Config | None = None) -> None:
        self._config = config or BM25Config()

    def rank(
        self,
        movies: list[Movie],
        corpus_tokens: list[list[str]],
        query_tokens: list[str],
        limit: int,
    ) -> list[SearchResult]:
        if limit <= 0 or not movies or not query_tokens:
            return []

        avgdl = (
            sum(len(tokens) for tokens in corpus_tokens) / len(corpus_tokens)
            if corpus_tokens
            else 0.0
        )
        if avgdl == 0.0:
            return []

        num_docs = len(movies)
        df = Counter[str]()
        for tokens in corpus_tokens:
            unique_tokens = set(tokens)
            for query_token in query_tokens:
                if query_token in unique_tokens:
                    df[query_token] += 1

        scored: list[SearchResult] = []
        for idx, movie in enumerate(movies):
            tokens = corpus_tokens[idx]
            doc_len = len(tokens)
            tf = Counter(tokens)

            score = 0.0
            for query_token in query_tokens:
                if df[query_token] > 0:
                    idf = math.log(
                        (num_docs - df[query_token] + 0.5) / (df[query_token] + 0.5) + 1.0
                    )
                    denominator = tf[query_token] + self._config.k1 * (
                        1 - self._config.b + self._config.b * doc_len / avgdl
                    )
                    if denominator > 0:
                        score += idf * (tf[query_token] * (self._config.k1 + 1)) / denominator
            if score > 0:
                scored.append(SearchResult(movie=movie, score=score))

        scored.sort(key=lambda item: (-item.score, item.movie.id))
        return scored[:limit]
