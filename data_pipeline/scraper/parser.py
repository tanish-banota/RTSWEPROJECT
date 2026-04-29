import json
from bs4 import BeautifulSoup
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def parse_events(raw_data=None):
    from config import RAW_PATH, CLEAN_PATH

    # Accept raw_data directly (pipeline chaining) or fall back to reading from disk
    if raw_data is None:
        try:
            with open(RAW_PATH, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
        except FileNotFoundError:
            print(
                f"Error: raw data file not found at {RAW_PATH}. Run fetcher first.")
            return None

    events_list = raw_data.get("value", [])
    clean_events = []

    for event in events_list:
        try:
            raw_start = event.get("startsOn")
            raw_end = event.get("endsOn")

            # GetInvolved returns times in Eastern time — parse into DateTime object and keep as-is
            dt_start = datetime.fromisoformat(raw_start)
            dt_end = datetime.fromisoformat(raw_end)

            clean_event = {
                "title": event.get("name", ""),
                "club_name": event.get("organizationName", ""),
                "description": clean_html(event.get("description", "")),
                "location": event.get("location", ""),
                "date": dt_start.strftime("%Y-%m-%d"),
                "start_time": dt_start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_time": dt_end.strftime("%Y-%m-%dT%H:%M:%S"),
                "source": "getinvolved"
            }

            clean_events.append(clean_event)
        except Exception as e:
            print(f"Skipping an event due to parsing error: {e}")
            continue

    # Check if an output clean file exists, if not create one
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CLEAN_PATH, "w", encoding="utf-8") as outfile:
        json.dump(clean_events, outfile, indent=4)

    print(f"Successfully cleaned {len(clean_events)} events!")
    return clean_events


if __name__ == "__main__":
    parse_events()
