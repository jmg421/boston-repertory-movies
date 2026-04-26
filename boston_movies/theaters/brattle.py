import requests
from bs4 import BeautifulSoup
from boston_movies.core import Film, HEADERS

NAME = "Brattle Theatre"

def fetch() -> list[Film]:
    r = requests.get("https://brattlefilm.org/", headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    films = []
    for show in soup.select("div.show"):
        link = show.select_one("a[href*='/movies/']")
        h2 = show.select_one("h2")
        if link and h2:
            title = h2.get_text(strip=True)
            subtitle_el = show.select_one("span.show__subtitle")
            subtitle = subtitle_el.get_text(strip=True) if subtitle_el else ""
            films.append(Film(title=title, theater=NAME, url=link["href"], subtitle=subtitle))
    return films
