# Boston Repertory Movies 🎬

Union list of current films at Boston-area repertory/arthouse theaters.

Built for [@OmicsOmicsBlog](https://x.com/OmicsOmicsBlog) who [tried to vibe-code this with Gemini and got dead code](https://omicsomics.blogspot.com/2026/04/crossing-vibicon.html). Fixed by [@JonIsGold](https://x.com/JonIsGold).

## Theaters

| Theater | Location | Source |
|---------|----------|--------|
| Brattle Theatre | Cambridge | HTML scrape |
| Coolidge Corner Theatre | Brookline | HTML scrape |
| Somerville Theatre | Somerville | RSS feed |
| Harvard Film Archive | Cambridge | HTML scrape |
| Alamo Drafthouse | Seaport | JSON API (coming soon) |

## Usage

```bash
pip install requests beautifulsoup4
python3 movies.py          # pretty-printed union list
python3 movies.py --json   # JSON output
```

## Want to add a theater?

Write a `fetch_yourtheater()` function that returns a list of `Film` objects. PRs welcome.
