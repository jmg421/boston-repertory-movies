from dataclasses import dataclass, asdict

HEADERS = {"User-Agent": "BostonRepMovies/1.0 (github.com/jmg421/boston-repertory-movies)"}

@dataclass
class Film:
    title: str
    theater: str
    url: str
    subtitle: str = ""
