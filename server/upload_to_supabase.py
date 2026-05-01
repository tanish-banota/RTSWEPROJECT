import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

load_dotenv()

# 1. Setup Supabase Connection
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") 

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

# Now the type checker knows 'url' and 'key' are definitely strings
supabase: Client = create_client(url, key)

def upload_events(source):
    # 2. Load your tagged data — accepts a list of events or a file path
    if isinstance(source, list):
        events = source
    else:
        if not os.path.exists(source):
            print(f"File not found: {source}")
            return
        with open(source, 'r', encoding='utf-8') as f:
            events = json.load(f)

    print(f"Syncing {len(events)} events to Supabase (Add/Update)...")

    success_count = 0
    failed_count = 0

    for event in events:
        try:
            # 3. Use .upsert() to handle updates
            # 'on_conflict' ensures that if (title + date) exists, it updates the tags/info
            supabase.table("events").upsert(
                event, 
                on_conflict="title,date"
            ).execute()
            
            success_count += 1
        except Exception as e:
            print(f"❌ Failed: {event.get('title')} | Error: {e}")
            failed_count += 1

    print(f"\n--- Sync Complete ---")
    print(f"Events Successfully Synced: {success_count}")
    if failed_count:
        print(f"Errors:                      {failed_count}")

if __name__ == "__main__":
    upload_events('server/tagged_events.json')