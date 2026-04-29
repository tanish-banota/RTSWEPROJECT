import json
import sys
from config import PROJECT_ROOT, CLEAN_PATH, TAGGED_PATH
from scraper.fetcher import fetch_events
from scraper.parser import parse_events
from scraper.discord_fetcher import fetch_discord_announcements
from scraper.discord_parser import parse_discord_messages

sys.path.insert(0, str(PROJECT_ROOT / "server"))


def run_pipeline():
    from tagging_engine import process_events_pipeline
    from upload_to_supabase import upload_events

    print("=== Starting Full Data Pipeline ===\n")

    print("Step 1/6: Fetching events from Anthology Engage API...")
    raw_data = fetch_events()
    if raw_data is None:
        print("Pipeline aborted: fetch failed.")
        return

    print("\nStep 2/6: Parsing and cleaning Anthology events...")
    clean_events = parse_events(raw_data)
    if not clean_events:
        print("Pipeline aborted: no events parsed.")
        return

    print("\nStep 3/6: Fetching Discord announcements...")
    discord_raw = fetch_discord_announcements()
    if discord_raw is None:
        print("Warning: Discord fetch failed or returned no messages. Continuing without Discord events.")
    else:
        print("\nStep 4/6: Parsing Discord announcements...")
        discord_events = parse_discord_messages(discord_raw)
        if discord_events:
            clean_events.extend(discord_events)
            print(f"Combined event total: {len(clean_events)}")

    # To make sure CLEAN_PATH has access to both getINVOLVED and DISCORD EVENTS
    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_events, f, indent=4)
    print(f"Combined clean data written to {CLEAN_PATH}")

    print("\nStep 5/6: Tagging events with AI...")
    process_events_pipeline(CLEAN_PATH, TAGGED_PATH)

    print("\nStep 6/6: Uploading tagged events to Supabase...")
    upload_events(TAGGED_PATH)

    print("\n=== Pipeline Complete ===")


if __name__ == "__main__":
    run_pipeline()
