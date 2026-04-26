import requests
from bs4 import BeautifulSoup
from boston_movies.core import Film, HEADERS
NAME = "Harvard Film Archive"
def fetch():
    r = requests.get("https://harvardfilmarchive.org/calendar", headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    films, seen = [], set()
    for event in soup.select(".event"):
        lines = [l.strip() for l in event.get_text("\n").split("\n") if l.strip() and l.strip() != "Read more"]
        for line in lines:
            if any(s in line for s in ["Directed by","Screening","pm","am","Sold Out"]) or line.startswith("$") or line == "-": continue
            if line not in seen and len(line) > 3:
                seen.add(line)
                films.append(Film(title=line, theater=NAME, url="https://harvardfilmarchive.org/calendar"))
    return films
