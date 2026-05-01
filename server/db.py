import os
from typing import Optional # <--- Add this import
from dotenv import load_dotenv
from supabase import create_client, Client

# Load variables from .env file
load_dotenv()

# Use the "Lead Dev" way to avoid type errors
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")

# Initialize the variable with the Optional type hint
# This prevents the "None is not assignable to Client" error later
supabase: Optional[Client] = None 

print("Supabase connection initialized.")

try:
    # Now assign the actual client
    supabase = create_client(url, key)
    
    # Test query
    test = supabase.table("events").select("*").limit(1).execute()
    print("Test query successful. Connection is working. Data: ", test.data)
    
except Exception as e:
    print(f"Test query failed: {e}")
    # Because we used Optional[Client], the IDE is now happy with this line:
    supabase = None