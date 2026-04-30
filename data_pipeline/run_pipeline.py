import json
import sys
from config import PROJECT_ROOT, CLEAN_PATH, TAGGED_PATH
from scraper.fetcher import fetch_events
from scraper.parser import parse_events
from scraper.discord_fetcher import fetch_discord_announcements
from scraper.discord_parser import parse_discord_messages
from scraper.groupme_fetcher import fetch_groupme_announcements
from scraper.groupme_parser import parse_groupme_messages

sys.path.insert(0, str(PROJECT_ROOT / "server"))


def run_pipeline():
    from tagging_engine import process_events_pipeline
    from upload_to_supabase import upload_events

    print("=== Starting Full Data Pipeline ===\n")

    # --- Anthology ---
    print("Step 1/8: Fetching events from Anthology Engage API...")
    raw_data = fetch_events()
    if raw_data is None:
        print("  Fetch failed. Falling back to cached disk data...")

    print("\nStep 2/8: Parsing and cleaning Anthology events...")
    # Optimal: raw_data passed in-memory. Fallback: raw_data=None → parser reads from disk.
    clean_events = parse_events(raw_data) or []
    if not clean_events:
        print("  Warning: No Anthology events available from fetch or disk.")

    # --- Discord ---
    print("\nStep 3/8: Fetching Discord announcements...")
    discord_raw = fetch_discord_announcements()
    if discord_raw is None:
        print("  Fetch failed. Falling back to cached disk data...")

    print("\nStep 4/8: Parsing Discord announcements...")
    # Optimal: discord_raw passed in-memory. Fallback: discord_raw=None → parser reads from disk.
    discord_events = parse_discord_messages(discord_raw) or []
    if discord_events:
        clean_events.extend(discord_events)
        print(f"  Combined event total: {len(clean_events)}")
    else:
        print("  Warning: No Discord events available from fetch or disk.")

    # --- GroupMe ---
    print("\nStep 5/8: Fetching GroupMe announcements...")
    groupme_raw = fetch_groupme_announcements()
    if groupme_raw is None:
        print("  Fetch failed. Falling back to cached disk data...")

    print("\nStep 6/8: Parsing GroupMe announcements...")
    # Optimal: groupme_raw passed in-memory. Fallback: groupme_raw=None → parser reads from disk.
    groupme_events = parse_groupme_messages(groupme_raw) or []
    if groupme_events:
        clean_events.extend(groupme_events)
        print(f"  Combined event total: {len(clean_events)}")
    else:
        print("  Warning: No GroupMe events available from fetch or disk.")

    if not clean_events:
        print("\nPipeline aborted: no events from any source.")
        return

    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_events, f, indent=4)
    print(f"\nCombined clean data written to {CLEAN_PATH}")

    print("\nStep 7/8: Tagging events with AI...")
    process_events_pipeline(CLEAN_PATH, TAGGED_PATH)

    print("\nStep 8/8: Uploading tagged events to Supabase...")
    upload_events(TAGGED_PATH)

    print("\n=== Pipeline Complete ===")


if __name__ == "__main__":
    run_pipeline()
