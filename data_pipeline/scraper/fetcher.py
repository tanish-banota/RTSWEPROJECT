from config import RAW_PATH
from datetime import datetime, timezone
import json
import requests
import sys
from pathlib import Path

# Connecting config.py to fetcher.py since the two files live in different folders
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def build_url(take=50):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    return (
        f"https://rutgers.campuslabs.com/engage/api/discovery/event/search"
        f"?endsAfter={requests.utils.quote(now)}"
        f"&orderByField=endsOn&orderByDirection=ascending"
        f"&status=Approved&take={take}&query="
    )


def fetch_events():
    url = build_url()

    # Mimic a browser to avoid automated request blocking.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    print("Fetching event data from Anthology Engage API...")

    try:
        # Data scrapping
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        raw_data = response.json()

        # Checking output file exists, if not then create one
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RAW_PATH, "w", encoding="utf-8") as file:
            json.dump(raw_data, file, indent=4)

        print(f"Success! Raw data saved to {RAW_PATH}")
        return raw_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None


if __name__ == "__main__":
    fetch_events()
