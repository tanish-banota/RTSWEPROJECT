import os
from typing import Dict, Any, List, cast
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if url is None or key is None:
    raise ValueError("CRITICAL: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing from .env")

supabase: Client = create_client(url, key)

def get_chat_history(event_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetches the last 50 messages for a specific event.
    """
    try:
        response = supabase.table("messages") \
            .select("*") \
            .eq("event_id", event_id) \
            .order("created_at") \
            .limit(limit) \
            .execute()
        
        # Fixed: Explicit cast to satisfy Pylance invariance check
        return cast(List[Dict[str, Any]], response.data)
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []

def send_chat_message(event_id: str, user_id: str, user_name: str, content: str) -> Dict[str, Any]:
    try:
        message_data = {
            "event_id": event_id,
            "user_id": user_id,
            "user_name": user_name,
            "content": content
        }
        response = supabase.table("messages").insert(message_data).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"status": "error", "message": str(e)}

def delete_chat_message(message_id: str, admin_id: str) -> Dict[str, Any]:
    try:
        admin_check = supabase.table("profiles").select("is_admin").eq("id", admin_id).single().execute()
        
        if admin_check.data and isinstance(admin_check.data, dict):
            if admin_check.data.get("is_admin") is True:
                supabase.table("messages").delete().eq("id", message_id).execute()
                return {"status": "success", "message": "Message deleted"}
        
        return {"status": "error", "message": "Unauthorized"}
    except Exception as e:
        print(f"Error in delete_chat_message: {e}")
        return {"status": "error", "message": str(e)}