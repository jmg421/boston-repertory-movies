#!/usr/bin/env python3
"""Boston Repertory Movie Listings — Union List"""
import json, argparse
from dataclasses import asdict
from datetime import datetime
from boston_movies.aggregator import get_all_films, dedupe

def main():
    parser = argparse.ArgumentParser(description="Boston repertory movie union list")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    all_films = get_all_films(quiet=args.json)

    if args.json:
        print(json.dumps([asdict(f) for f in all_films], indent=2))
        return

    union = dedupe(all_films)

    print(f"\n{'='*60}")
    print(f"🎬 Boston Repertory Movies — {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"{'='*60}\n")

    multi = {k: v for k, v in union.items() if len(v) > 1}
    if multi:
        print("🎯 Playing at multiple theaters:\n")
        for key, films in sorted(multi.items()):
            print(f"  {films[0].title}")
            print(f"    📍 {', '.join(f.theater for f in films)}")
            for f in films:
                print(f"    🔗 {f.url}")
            print()

    print(f"📋 All listings ({len(union)} unique films):\n")
    for key, films in sorted(union.items()):
        f = films[0]
        extra = f" + {len(films)-1} more" if len(films) > 1 else ""
        print(f"  • {f.title} — {f.theater}{extra}")

    print(f"\n{'='*60}")
    print(f"Total: {len(all_films)} listings, {len(union)} unique films")

if __name__ == "__main__":
    main()
