import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load variables from .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")

# Initialize the Supabase client
# This 'supabase' object can now be imported by your other scripts
supabase: Client = create_client(url, key)

print("Supabase connection initialized.")

try:
    test = supabase.table("events").select("*").limit(1).execute()
    print("Test query successful. Connection is working. Data: ", test.data)
except Exception as e:
    print(f"Test query failed: {e}")
    supabase = None
    