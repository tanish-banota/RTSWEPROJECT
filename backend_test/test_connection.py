import os
from dotenv import load_dotenv
from supabase import create_client

# 1. Load your credentials
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 2. "Fake" Scraped Data
mock_event = {
    "title": "Initial Connection Test",
    "location": "Busch Student Center",
    "description": "If you see this, the bridge is working!",
    "source": "manual_test"
}

# 3. Push to the Server
try:
    response = supabase.table("events").insert(mock_event).execute()
    print("Success! Check your Supabase dashboard.")
except Exception as e:
    print(f"Connection failed: {e}")