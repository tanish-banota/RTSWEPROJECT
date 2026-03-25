import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# 1. Setup Supabase Connection
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") 
supabase: Client = create_client(url, key)

def upload_events(json_file):
    # 2. Load your tagged data
    with open(json_file, 'r') as f:
        events = json.load(f)

    print(f"Checking {len(events)} events for upload...")

    success_count = 0
    skipped_count = 0

    # 3. Loop through each event to handle duplicates individually
    for event in events:
        try:
            # Attempt to insert a single event
            supabase.table("events").insert(event).execute()
            print(f"✅ Uploaded: {event['title']}")
            success_count += 1
        except Exception as e:
            # Check if it's a duplicate error (unique_event_listing is our constraint name)
            if "unique_event_listing" in str(e):
                print(f"⏭️  Skipped (Duplicate): {event['title']}")
                skipped_count += 1
            else:
                print(f"❌ Failed: {event['title']} | Error: {e}")

    print(f"\n--- Upload Complete ---")
    print(f"New events added: {success_count}")
    print(f"Duplicates skipped: {skipped_count}")

if __name__ == "__main__":
    upload_events('server/tagged_events.json')