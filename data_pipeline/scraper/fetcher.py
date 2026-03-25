import requests
import json
from pathlib import Path


def fetch_events():
    # URL gotten for scrapping after API Interception
    url = "https://rutgers.campuslabs.com/engage/api/discovery/event/search?endsAfter=2026-03-24T14%3A05%3A10-04%3A00&orderByField=endsOn&orderByDirection=ascending&status=Approved&take=15&query="

    # Websites often block automated requests.
    # Passing a standard User-Agent header mimics a normal web browser.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    print("Fetching event data from Anthology Engage API...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Catch HTTP errors like 404

        # Parse the response into a Python dictionary(JSON format)
        raw_data = response.json()

        # --- UPDATED SECTION START ---
        # 1. Anchor to the data_pipeline directory
        SCRIPT_DIR = Path(__file__).resolve().parent
        PIPELINE_DIR = SCRIPT_DIR.parent
        # 2. Build the absolute path to your raw.json file
        file_path = PIPELINE_DIR / "data" / "raw" / "raw.json"

        # 3. Ensure the nested directories exist before saving
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # --- UPDATED SECTION END ---

        # Export the raw JSON onto the file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(raw_data, file, indent=4)

        print(f"Success! Raw data saved to {file_path}")
        return raw_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None


if __name__ == "__main__":
    fetch_events()
