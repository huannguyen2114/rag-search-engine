import math
import string
from collections import Counter

from cli.lib.search_util import load_movies, load_stopwords
from dto.movie import MovieDTO


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    translator = str.maketrans("", "", string.punctuation)
    tokens = text.lower().translate(translator).split()
    return [t for t in tokens if t not in stopwords]


def search_by_keyword(query: str, number_of_results: int = 5) -> list[MovieDTO]:
    movies = load_movies()
    stopwords = load_stopwords()

    query_tokens = tokenize(query, stopwords)

    if not query_tokens:
        if query.strip() == "":
            return movies[:number_of_results]
        return []

    # BM25 parameters
    k1 = 1.5
    b = 0.75

    # Prepare corpus
    corpus_tokens = [tokenize(f"{m.title} {m.description}", stopwords) for m in movies]
    avgdl = sum(len(tokens) for tokens in corpus_tokens) / len(corpus_tokens) if corpus_tokens else 0
    n = len(movies)

    # Document frequencies for query tokens
    df = Counter()
    for tokens in corpus_tokens:
        unique_tokens = set(tokens)
        for qt in query_tokens:
            if qt in unique_tokens:
                df[qt] += 1

    # Calculate BM25 scores
    scores = []
    for i, movie in enumerate(movies):
        tokens = corpus_tokens[i]
        doc_len = len(tokens)
        tf = Counter(tokens)
        score = 0
        for qt in query_tokens:
            if df[qt] > 0:
                idf = math.log((n - df[qt] + 0.5) / (df[qt] + 0.5) + 1.0)
                score += idf * (tf[qt] * (k1 + 1)) / (tf[qt] + k1 * (1 - b + b * doc_len / avgdl))
        if score > 0:
            scores.append((movie, score))

    # Sort by score descending, then by id ascending for stability
    scores.sort(key=lambda x: (-x[1], x[0].id))

    return [s[0] for s in scores[:number_of_results]]
