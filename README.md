# Gelbe Seiten Scraper in Python: German Business Leads as JSON or CSV

Python and Node examples for pulling **German B2B leads from Gelbe Seiten (gelbeseiten.de)** by category (Branche) and city: name, phone, email, website, address, rating, opening hours and services, one row per business. `example.py` also ranks the results for outreach and writes a CSV.

> Disclosure: I built this actor. It's a paid tool on Apify: https://apify.com/rel8ble/gelbe-seiten-scraper

## Quick start (Python)

```bash
pip install -r requirements.txt
export APIFY_TOKEN=<YOUR_APIFY_TOKEN>
python example.py --categories Elektriker Steuerberater --locations Berlin --max 50
```

Or try it with no token on the included sample of 12 real company rows:

```bash
python example.py --from-json sample-output.json
```

The core call is short:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("rel8ble/gelbe-seiten-scraper").call(run_input={
    "categories": ["Elektriker"],
    "locations": ["Berlin"],
    "maxResultsPerSearch": 50,
    "requireEmail": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(row["name"], row["phone"], row["email"], row["website"])
```

## Node

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('rel8ble/gelbe-seiten-scraper').call({
    categories: ['Steuerberater'],
    locations: ['München'],
    maxResultsPerSearch: 50,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.length, items[0]?.name);
```

## Input

| Field | Type | Default | What it does |
|---|---|---|---|
| `categories` | array | `["Elektriker"]` | Gelbe Seiten categories, in German (`Zahnarzt`, not `dentist`) |
| `locations` | array | `["Berlin"]` | German cities |
| `startUrls` | array | none | Gelbe Seiten URLs, instead of categories and cities |
| `maxResultsPerSearch` | integer | 100 | Max businesses per category and city |
| `scrapeDetails` | boolean | true | Open each business page (email, hours, fax, services) |
| `requireEmail` / `requireWebsite` / `requirePhone` | boolean | false | Keep only businesses that have this field |
| `minRating` | number | none | Minimum rating |

## Output

A real row from the actor's sample run (`Elektriker` in Berlin), trimmed from 38 fields:

```json
{
  "name": "Bahrke Elektroinstallation u. -geräte GmbH",
  "category": "Elektroinstallationen",
  "phone": "030 82 70 30 30",
  "phoneE164": "+493082703030",
  "email": "bahrke-berlin@t-online.de",
  "website": "http://www.bahrke-elektro.de",
  "address": "Blissestr. 60, 10713 Berlin",
  "district": "Wilmersdorf",
  "latitude": 52.479816,
  "longitude": 13.319864,
  "rating": 5,
  "reviewCount": 2,
  "services": ["Ladenbau"],
  "lastUpdated": "2026-06-01",
  "searchCategory": "Elektriker"
}
```

In the actor's 20-row sample run: phone 20, email 20, website 17, rating 9. `sample-output.json` keeps only the 12 incorporated companies from that run. It is a small sample, so expect other categories and cities to differ.

## What example.py does

It ranks businesses by how easy they are to reach and how much public signal they have:

- 3 points for an email, 2 for a website, 1 for a phone number
- 1 point for 5+ reviews, plus 1 for a rating of 4.5 or more
- 1 point for a listing updated within the past two years

The score is a simple sorting aid I chose, not a measure of lead quality. Change the weights to suit your outreach.

## Pricing

$0.35 per 1,000 businesses as of 3 Nov 2026, with no start fee, business-page details included. Check the [Store page](https://apify.com/rel8ble/gelbe-seiten-scraper) for the current price.

## Limits

- Germany only, and categories must be Gelbe Seiten's German names.
- Up to 5,000 businesses per category and city; split big cities by district.
- Business contact data of sole traders can be personal data under the GDPR, and German law limits unsolicited ads by email and phone. Check your outreach rules before contacting anyone.

## More

- Tutorial on dev.to: https://dev.to/rel8ble/building-german-b2b-lead-lists-from-gelbe-seiten-with-python-12h2
- Other B2B examples: [northdata-scraper-python](https://github.com/Rel8ble/northdata-scraper-python), [alibaba-supplier-search-scraper-python](https://github.com/Rel8ble/alibaba-supplier-search-scraper-python), [hktdc-sourcing-scraper-python](https://github.com/Rel8ble/hktdc-sourcing-scraper-python)

Need a custom scraper or a ready dataset? Hire me on Fiverr: https://www.fiverr.com/rel8ble
