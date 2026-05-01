import os
from typing import Optional, List, Any
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# 1. Type-safe Key Retrieval
url_env = os.getenv("SUPABASE_URL")
key_env = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url_env or not key_env:
    raise ValueError("❌ Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

# 2. Initialize Client
supabase: Client = create_client(url_env, key_env)

def promote_to_admin(email: str) -> None:
    print(f"🔍 Searching for: {email}...")
    
    try:
        # Fetch data
        response = supabase.table("profiles").select("id").eq("email", email).execute()
        
        # 3. Explicit Type Guard: This satisfies Pylance by proving 'data' is a non-empty list
        data = response.data
        if not isinstance(data, list) or len(data) == 0:
            print(f"❌ Could not find a profile with email: {email}")
            return

        # 4. Safe access
        first_row = data[0]
        if not isinstance(first_row, dict):
            print("❌ Unexpected data format received.")
            return

        user_id = first_row.get('id')
        if not user_id:
            print("❌ ID field missing in profile data.")
            return

        # 5. Execute Update
        supabase.table("profiles").update({"is_admin": True}).eq("id", user_id).execute()
        print(f"✅ Success! {email} (ID: {user_id}) is now an Admin.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Ensure this is your actual login email from the profiles table
    promote_to_admin("banotatanish@gmail.com")