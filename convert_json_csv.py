import json
import csv

def extract_city_state(street):
    """
    gets city and state from an address formatted like:
    '123 Main St, Honolulu, HI 96826'
    """
    if not street:
        return "", ""

    parts = [p.strip() for p in street.split(",")]

    # Need at least 3 parts to extract city/state
    if len(parts) < 3:
        return "", ""

    # city is second last element
    city = parts[-2]

    # state is first token in the last element (before ZIP)
    state_zip = parts[-1].split()
    state = state_zip[0] if state_zip else ""

    return city, state.upper()


with open("zillow_scraped.json", "r") as f:
    data = json.load(f)

rows = data["results"]

columns = [
    "price",
    "bedrooms",
    "dwell_type",
    "street",
    "neighborhood",
    "furniture",
    "title",
    "square_feet",
    "cityname",
    "state"
]

with open("apartments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()

    for row in rows:
        out = {}

        # copy direct fields
        for col in columns:
            if col not in ("square_feet", "city", "state"):
                out[col] = row.get(col, "")

        # square_feet gotten from "size"
        out["square_feet"] = row.get("size", "")

        # get city/state from street
        city, state = extract_city_state(row.get("street", ""))
        out["cityname"] = city
        out["state"] = state

        writer.writerow(out)

