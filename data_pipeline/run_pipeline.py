import sys
from config import PROJECT_ROOT, CLEAN_PATH, TAGGED_PATH
from scraper.fetcher import fetch_events
from scraper.parser import parse_events

sys.path.insert(0, str(PROJECT_ROOT / "server"))


def run_pipeline():
    from tagging_engine import process_events_pipeline
    from upload_to_supabase import upload_events

    print("=== Starting Full Data Pipeline ===\n")

    print("Step 1/4: Fetching events from Anthology Engage API...")
    raw_data = fetch_events()
    if raw_data is None:
        print("Pipeline aborted: fetch failed.")
        return

    print("\nStep 2/4: Parsing and cleaning events...")
    clean_events = parse_events(raw_data)
    if not clean_events:
        print("Pipeline aborted: no events parsed.")
        return

    print("\nStep 3/4: Tagging events with AI...")
    process_events_pipeline(CLEAN_PATH, TAGGED_PATH)

    print("\nStep 4/4: Uploading tagged events to Supabase...")
    upload_events(TAGGED_PATH)

    print("\n=== Pipeline Complete ===")


if __name__ == "__main__":
    run_pipeline()
