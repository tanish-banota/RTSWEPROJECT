import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# 1. Setup Supabase Connection
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") 
supabase: Client = create_client(url, key)

def upload_events(source):
    # 2. Load your tagged data — accepts a list of events or a file path
    if isinstance(source, list):
        events = source
    else:
        with open(source, 'r') as f:
            events = json.load(f)

    print(f"Uploading {len(events)} events to Supabase...")

    success_count = 0
    skipped_count = 0
    failed_count = 0

    for event in events:
        try:
            supabase.table("events").insert(event).execute()
            success_count += 1
        except Exception as e:
            if "23505" in str(e) or "unique_event_listing" in str(e):
                skipped_count += 1
            else:
                print(f"❌ Failed: {event.get('title')} | Error: {e}")
                failed_count += 1

    print(f"\n--- Upload Complete ---")
    print(f"New events added: {success_count}")
    print(f"Already in DB (skipped): {skipped_count}")
    if failed_count:
        print(f"Errors: {failed_count}")

if __name__ == "__main__":
    upload_events('server/tagged_events.json')