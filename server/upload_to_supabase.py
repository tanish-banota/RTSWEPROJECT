import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# 1. Setup Supabase Connection
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use Service Role Key for backend scripts
supabase: Client = create_client(url, key)

def upload_events(json_file):
    # 2. Load your tagged data
    with open(json_file, 'r') as f:
        events = json.load(f)

    print(f"Uploading {len(events)} events to Supabase...")

    # 3. Push to the 'events' table
    # Supabase handles the Python list -> SQL array conversion automatically!
    try:
        response = supabase.table("events").insert(events).execute()
        print("Successfully uploaded events!")
        return response
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    upload_events('server/tagged_events.json')