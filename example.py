"""Pull German business leads from Gelbe Seiten, rank them for outreach, write a CSV.

Live:   APIFY_TOKEN=... python example.py --categories Elektriker --locations Berlin --max 50
Sample: python example.py --from-json sample-output.json
"""
import argparse
import csv
import json
import os
from datetime import date, timedelta

ACTOR = "rel8ble/gelbe-seiten-scraper"
COLUMNS = ["score", "name", "category", "phone", "email", "website", "address", "rating", "reviewCount", "lastUpdated", "url"]


def fetch(categories, locations, max_results):
    from apify_client import ApifyClient

    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(run_input={
        "categories": categories,
        "locations": locations,
        "maxResultsPerSearch": max_results,
    })
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())


def score(row, today=None):
    today = today or date.today()
    points = 0
    points += 3 if row.get("email") else 0
    points += 2 if row.get("website") else 0
    points += 1 if row.get("phone") else 0
    points += 1 if (row.get("reviewCount") or 0) >= 5 else 0
    points += 1 if (row.get("rating") or 0) >= 4.5 else 0
    updated = row.get("lastUpdated")
    if updated and date.fromisoformat(updated[:10]) >= today - timedelta(days=730):
        points += 1
    return points


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--categories", nargs="+", default=["Elektriker"])
    parser.add_argument("--locations", nargs="+", default=["Berlin"])
    parser.add_argument("--max", type=int, default=50)
    parser.add_argument("--from-json", help="read rows from a saved file instead of calling the actor")
    parser.add_argument("--out", default="gelbe_seiten_leads.csv")
    args = parser.parse_args()

    if args.from_json:
        with open(args.from_json, encoding="utf-8") as f:
            rows = json.load(f)
    else:
        rows = fetch(args.categories, args.locations, args.max)

    for row in rows:
        row["score"] = score(row)
    rows.sort(key=lambda r: (-r["score"], -(r.get("reviewCount") or 0)))

    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} businesses -> {args.out}")
    for row in rows[:5]:
        print(f"{row['score']:>2}  {row['name']}  ({row.get('rating') or '-'}, {row.get('reviewCount') or 0} reviews)  {row.get('email') or '-'}")


if __name__ == "__main__":
    main()
