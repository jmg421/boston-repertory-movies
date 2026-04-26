import re, html, requests
from boston_movies.core import Film, HEADERS
NAME = "Somerville Theatre"
def fetch():
    films = []
    try:
        r = requests.get("https://www.somervilletheatre.com/feed/reportory-films", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', r.text)
            if not titles: titles = re.findall(r'<title>(.*?)</title>', r.text)
            links = re.findall(r'<link>(https://www\.somervilletheatre\.com/[^<]+)</link>', r.text)
            for i, title in enumerate(titles):
                if title and "Somerville Theatre" not in title and len(title) > 3:
                    url = links[i] if i < len(links) else "https://www.somervilletheatre.com/movies/"
                    films.append(Film(title=html.unescape(title.strip()), theater=NAME, url=url))
    except Exception: pass
    return films
