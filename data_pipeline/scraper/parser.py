import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timezone


def clean_html(raw_html):
    # If the text is empty or None, return an empty string
    if not raw_html:
        return ""

    # Parse the HTML and extract plain text
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def parse_events():
    # 1. Load Raw Data
    with open("data/raw/raw.json", "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    # 2. Isolate all other data except the values we need.
    # If cannot find value, don't return error, rather a []
    events_list = raw_data.get("value", [])

    clean_events = []

    # 4. Iterate and Clean
    for event in events_list:
        try:
            # Extract basic text, same logic as earlier, return "" if no value found
            raw_title = event.get("name", "")
            raw_desc = event.get("description", "")
            raw_org = event.get("organizationName", "")
            raw_location = event.get("location", "")

            # --- Time Formatting ---
            raw_start = event.get("startsOn")
            raw_end = event.get("endsOn")

            # Change the string into a datetime object so we can use datetime library
            dt_obj_start = datetime.fromisoformat(raw_start)
            dt_obj_end = datetime.fromisoformat(raw_end)

            # Convert to UTC
            dt_utc_start = dt_obj_start.astimezone(timezone.utc)
            dt_utc_end = dt_obj_end.astimezone(timezone.utc)

            # Format outputs for Supabase
            formatted_date = dt_utc_start.strftime("%Y-%m-%d")
            formatted_time_start = dt_utc_start.strftime("%Y-%m-%dT%H:%M:%SZ")
            formatted_time_end = dt_utc_end.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Building the JSON format wanted for clean data
            clean_event = {
                "title": raw_title,
                "club_name": raw_org,
                # Here have to use this weird if/else format due to the work being done inside a dictionary
                "description": clean_html(raw_desc) if raw_desc else "",
                "location": raw_location,
                "date": formatted_date,
                "start_time": formatted_time_start,
                "end_time": formatted_time_end,
                "source": "getinvolved"
            }

            clean_events.append(clean_event)
        # Exception handling
        except Exception as e:
            print(f"Skipping an event due to parsing error: {e}")
            continue

    # 5. Export Clean Data
    os.makedirs("data/clean", exist_ok=True)  # Making sure folder exists
    with open("data/clean/clean.json", "w", encoding="utf-8") as outfile:
        json.dump(clean_events, outfile, indent=4)

    print(f"Successfully cleaned {len(clean_events)} events!")


if __name__ == "__main__":
    parse_events()
