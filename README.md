# Boston Repertory Movies 🎬

Union list of current films at Boston-area repertory/arthouse theaters.

Built for [@OmicsOmicsBlog](https://x.com/OmicsOmicsBlog) who [tried to vibe-code this with Gemini and got dead code](https://omicsomics.blogspot.com/2026/04/crossing-vibicon.html). Fixed by [@JonIsGold](https://x.com/JonIsGold) — a coder learning omics, returning the favor for a biologist learning to vibe code.

## Theaters

| Theater | Location | Site |
|---------|----------|------|
| Brattle Theatre | Cambridge | brattlefilm.org |
| Coolidge Corner Theatre | Brookline | coolidge.org |
| Somerville Theatre | Somerville | somervilletheatre.com |

## Usage

```bash
pip install requests beautifulsoup4
python3 movies.py          # pretty-printed union list
python3 movies.py --json   # JSON output
```

## How It Works

No APIs — these theaters serve HTML. The script fetches each theater's showtimes page, parses the film listings with BeautifulSoup, deduplicates by title, and generates a union list highlighting films playing at multiple theaters.

## Want to add a theater?

Write a `fetch_yourtheater()` function that returns a list of `Film` objects. PRs welcome.
