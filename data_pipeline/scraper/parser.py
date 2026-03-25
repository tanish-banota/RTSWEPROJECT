import json
from pathlib import Path
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

    # --- UPDATED PATHING SECTION START ---
    # Anchor to the data_pipeline directory
    SCRIPT_DIR = Path(__file__).resolve().parent
    PIPELINE_DIR = SCRIPT_DIR.parent

    # Build dynamic paths for both reading and writing
    raw_file_path = PIPELINE_DIR / "data" / "raw" / "raw.json"
    clean_file_path = PIPELINE_DIR / "data" / "clean" / "clean.json"
    # --- UPDATED PATHING SECTION END ---

    # Load Raw Data
    with open(raw_file_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    # Isolate all other data except the values we need.
    # If cannot find value, don't return error, rather a []
    events_list = raw_data.get("value", [])

    clean_events = []

    # Iterate and Clean
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

    # Export Clean Data
    # Making sure folder exists
    clean_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(clean_file_path, "w", encoding="utf-8") as outfile:
        json.dump(clean_events, outfile, indent=4)

    print(f"Successfully cleaned {len(clean_events)} events!")


if __name__ == "__main__":
    parse_events()
