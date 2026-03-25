from flask import Flask, jsonify
from flask_cors import CORS
from db import supabase

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/events', methods=['GET'])
def get_events():
    """Fetch all events from Supabase"""
    try:
        response = supabase.table("events").select("*").execute()
        events = response.data
        
        # Transform the data to match the frontend format
        formatted_events = []
        for event in events:
            formatted_events.append({
                "id": str(event.get("id", "")),
                "title": event.get("title", ""),
                "date": event.get("date", ""),
                "club": event.get("club", ""),
                "location": event.get("location", "")
            })
        
        return jsonify(formatted_events), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
