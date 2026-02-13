import string

from nltk import PorterStemmer

_TRANSLATOR = str.maketrans("", "", string.punctuation)
_STEMMER = PorterStemmer()


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    tokens = text.lower().translate(_TRANSLATOR).split()
    return [_STEMMER.stem(token) for token in tokens if token not in stopwords]
