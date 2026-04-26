#!/usr/bin/env python3
"""
Boston Repertory Movie Listings — Union List

Fetches current listings from Boston-area repertory/arthouse theaters
and generates a unified list. Built for Keith Robison (@OmicsOmicsBlog)
who tried to vibe-code this with Gemini and got dead code.

Theaters:
  - Brattle Theatre (Cambridge)
  - Coolidge Corner Theatre (Brookline)
  - Somerville Theatre (Somerville)

Usage:
    python3 movies.py
    python3 movies.py --json
"""

import re, json, argparse, html, html
from datetime import datetime
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "BostonRepMovies/1.0 (github.com/nodesbio/boston-repertory-movies)"}


@dataclass
class Film:
    title: str
    theater: str
    url: str
    subtitle: str = ""


def fetch_brattle() -> list[Film]:
    """Brattle Theatre — WordPress + Filmbot Hall."""
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
            films.append(Film(title=title, theater="Brattle Theatre", url=link["href"], subtitle=subtitle))
    return films


def fetch_coolidge() -> list[Film]:
    """Coolidge Corner Theatre — Drupal, server-rendered."""
    r = requests.get("https://coolidge.org/showtimes", headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    films = []
    seen = set()
    for card in soup.select("div.film-card"):
        link = card.select_one("a.film-card__link")
        if not link:
            continue
        title = link.get("title", "").strip()
        href = link.get("href", "")
        if not title or title in seen:
            continue
        seen.add(title)
        films.append(Film(title=title, theater="Coolidge Corner", url=f"https://coolidge.org{href}"))
    return films


def fetch_somerville() -> list[Film]:
    """Somerville Theatre — repertory calendar is PDF-only, no HTML listings.
    We scrape their feed for any repertory film posts instead."""
    films = []
    try:
        r = requests.get("https://www.somervilletheatre.com/feed/reportory-films", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            # RSS feed — extract titles
            titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', r.text)
            if not titles:
                titles = re.findall(r'<title>(.*?)</title>', r.text)
            links = re.findall(r'<link>(https://www\.somervilletheatre\.com/[^<]+)</link>', r.text)
            for i, title in enumerate(titles):
                if title and "Somerville Theatre" not in title and len(title) > 3:
                    url = links[i] if i < len(links) else "https://www.somervilletheatre.com/movies/"
                    films.append(Film(title=html.unescape(title.strip()), theater="Somerville Theatre", url=url))
    except Exception:
        pass
    return films


def fetch_harvard() -> list[Film]:
    """Harvard Film Archive — calendar page with event classes."""
    r = requests.get("https://harvardfilmarchive.org/calendar", headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    films = []
    seen = set()
    for event in soup.select(".event"):
        lines = [l.strip() for l in event.get_text("\n").split("\n") if l.strip() and l.strip() != "Read more"]
        # Film title is after the time (e.g. "7:00 pm"), usually index 2
        for line in lines:
            if "Directed by" in line or "Screening" in line or "pm" in line or "am" in line or line.startswith("$") or line == "-" or "Sold Out" in line:
                continue
            if line not in seen and len(line) > 3:
                seen.add(line)
                films.append(Film(title=line, theater="Harvard Film Archive", url="https://harvardfilmarchive.org/calendar"))
    return films


def fetch_alamo() -> list[Film]:
    """Alamo Drafthouse Boston — JSON schedule API."""
    r = requests.get("https://drafthouse.com/s/mother/v2/schedule/market/boston", headers=HEADERS, timeout=15)
    films = []
    seen = set()
    try:
        data = r.json()
        for p in data.get("data", data).get("presentations", data.get("presentations", [])):
            slug = p.get("slug", "")
            show = p.get("show") or {}
            title = show.get("title", "")
            # Clean HTML tags from title
            title = re.sub(r'<[^>]+>', '', title).strip()
            if not title:
                title = slug.replace("-", " ").title()
            if title and title not in seen and len(title) > 3:
                # Filter out non-movie items
                skip = ['all ages', 'qr ordering', 'rated pg', 'costume screening']
                if title.lower() in skip:
                    continue
                seen.add(title)
                films.append(Film(title=title, theater="Alamo Drafthouse", url=f"https://drafthouse.com/boston/show/{slug}"))
    except Exception:
        pass
    return films


def main():
    parser = argparse.ArgumentParser(description="Boston repertory movie union list")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    theaters = [
        ("Brattle Theatre", fetch_brattle),
        ("Coolidge Corner", fetch_coolidge),
        ("Somerville Theatre", fetch_somerville),
        ("Harvard Film Archive", fetch_harvard),
        ("Alamo Drafthouse", fetch_alamo),
    ]

    all_films: list[Film] = []
    for name, fetcher in theaters:
        try:
            films = fetcher()
            all_films.extend(films)
            if not args.json:
                print(f"✅ {name}: {len(films)} films")
        except Exception as e:
            if not args.json:
                print(f"❌ {name}: {e}")

    if args.json:
        print(json.dumps([asdict(f) for f in all_films], indent=2))
        return

    # Union list — dedupe by normalized title
    print(f"\n{'='*60}")
    print(f"🎬 Boston Repertory Movies — {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"{'='*60}\n")

    # Group by title (case-insensitive)
    union: dict[str, list[Film]] = {}
    for f in all_films:
        key = re.sub(r'\s+', ' ', f.title.lower().strip())
        union.setdefault(key, []).append(f)

    # Films at multiple theaters first
    multi = {k: v for k, v in union.items() if len(v) > 1}
    single = {k: v for k, v in union.items() if len(v) == 1}

    if multi:
        print("🎯 Playing at multiple theaters:\n")
        for key, films in sorted(multi.items()):
            theaters_str = ", ".join(f.theater for f in films)
            print(f"  {films[0].title}")
            print(f"    📍 {theaters_str}")
            for f in films:
                print(f"    🔗 {f.url}")
            print()

    print(f"📋 All listings ({len(union)} unique films):\n")
    for key, films in sorted(union.items()):
        f = films[0]
        extra = f" + {len(films)-1} more" if len(films) > 1 else ""
        print(f"  • {f.title} — {f.theater}{extra}")
        if f.subtitle:
            print(f"    {f.subtitle}")

    print(f"\n{'='*60}")
    print(f"Total: {len(all_films)} listings across {len(theaters)} theaters, {len(union)} unique films")


if __name__ == "__main__":
    main()
