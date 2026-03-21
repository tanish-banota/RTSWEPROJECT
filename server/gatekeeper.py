def add_new_event(user_id, event_data):
    # 1. The Gatekeeper: Check the profile role
    profile = supabase.table("profiles").select("role").eq("id", user_id).single().execute()
    
    if profile.data and profile.data.get("role") == "admin":
        # 2. Proceed with the insert if they are an admin
        result = supabase.table("events").insert(event_data).execute()
        print("Event added successfully!")
        return result
    else:
        # 3. Block the action if they are just a student
        print("Access Denied: You do not have admin privileges.")
        return None

# --- TESTING IT ---
# Use your own UUID from the Supabase dashboard to test
my_admin_id = "a4b5b9eb-d1bb-485b-a494-ed15600fa85f" 
sample_event = {
    "title": "Admin Only Workshop",
    "description": "Only admins can post this.",
    "date": "2026-04-01"
}

add_new_event(my_admin_id, sample_event)