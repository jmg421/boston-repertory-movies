import re, requests
from boston_movies.core import Film, HEADERS
NAME = "Alamo Drafthouse"
def fetch():
    r = requests.get("https://drafthouse.com/s/mother/v2/schedule/market/boston", headers=HEADERS, timeout=15)
    films, seen = [], set()
    try:
        data = r.json()
        for p in data.get("data", data).get("presentations", []):
            slug = p.get("slug", "")
            show = p.get("show") or {}
            title = re.sub(r'<[^>]+>', '', show.get("title", "")).strip()
            if not title: title = slug.replace("-", " ").title()
            if title and title not in seen and len(title) > 3:
                if title.lower() in ('all ages','qr ordering','rated pg','costume screening'): continue
                seen.add(title)
                films.append(Film(title=title, theater=NAME, url=f"https://drafthouse.com/boston/show/{slug}"))
    except Exception: pass
    return films
