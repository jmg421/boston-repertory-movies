import re
from boston_movies.core import Film
from boston_movies.theaters import get_theaters

def get_all_films(quiet=False):
    all_films = []
    for name, fetcher in get_theaters():
        try:
            films = fetcher()
            all_films.extend(films)
            if not quiet: print(f"✅ {name}: {len(films)} films")
        except Exception as e:
            if not quiet: print(f"❌ {name}: {e}")
    return all_films

def dedupe(films):
    union = {}
    for f in films:
        key = re.sub(r'\s+', ' ', f.title.lower().strip())
        union.setdefault(key, []).append(f)
    return union
