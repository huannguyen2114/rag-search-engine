from movie_search.domain.tokenization import tokenize


def test_tokenize_lowercase_punctuation_stopwords_and_stemming() -> None:
    stopwords = {"the", "and"}
    tokens = tokenize("The runners, and running!", stopwords)
    assert tokens == ["runner", "run"]


def test_tokenize_empty_text() -> None:
    assert tokenize("", {"the"}) == []
