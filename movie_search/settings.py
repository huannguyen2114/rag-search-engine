from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / "cache"
MOVIES_PATH = DATA_DIR / "movies.json"
STOPWORDS_PATH = DATA_DIR / "stopwords.txt"
