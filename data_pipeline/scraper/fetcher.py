from datetime import datetime, timezone
from urllib.parse import quote
import requests
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def fetch_events():
    from config import RAW_PATH

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    url = (
        f"https://rutgers.campuslabs.com/engage/api/discovery/event/search"
        f"?endsAfter={quote(now)}"
        f"&orderByField=endsOn&orderByDirection=ascending"
        f"&status=Approved&take=15&query="
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    print("Fetching event data from Anthology Engage API...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        raw_data = response.json()

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
