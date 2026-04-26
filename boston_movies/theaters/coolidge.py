import requests
from bs4 import BeautifulSoup
from boston_movies.core import Film, HEADERS
NAME = "Coolidge Corner"
def fetch():
    r = requests.get("https://coolidge.org/showtimes", headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    films, seen = [], set()
    for card in soup.select("div.film-card"):
        link = card.select_one("a.film-card__link")
        if not link: continue
        title = link.get("title", "").strip()
        if not title or title in seen: continue
        seen.add(title)
        films.append(Film(title=title, theater=NAME, url=f"https://coolidge.org{link.get('href','')}"))
    return films
