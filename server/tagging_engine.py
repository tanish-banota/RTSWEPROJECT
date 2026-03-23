import os
import json
from google import genai
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Setup the Client with the specific 2026 model we found
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CURRENT_MODEL = "gemini-2.5-flash"

def generate_tags(event, use_ai=True):
    title = event.get('title', 'No Title')
    description = event.get('description', '')
    club = event.get('club_name', 'Unknown Club')
        
    if not use_ai:
        return ["academic"]

    prompt = f"""
    Categorize this Rutgers event for students:
    Club: {club}
    Title: {title}
    Description: {description}
    
    Return only a comma-separated list of tags (e.g., computer science, networking, pre-med).
    """
    
    try:
        # Call the Gemini 2.5 model
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=prompt
        )
        # Clean the string and turn it into a Python list
        tag_list = [t.strip().lower() for t in response.text.split(",")]
        return tag_list
    except Exception as e:
        print(f"AI Error for '{title}': {e}")
        # Fallback to local if AI fails
        return generate_tags(title, description, use_ai=False)

def process_events_pipeline(input_filename, output_filename):
    """
    The main 'Backend Lead' logic: Reads raw JSON, tags everything, saves new JSON.
    """
    # Load your sample data
    try:
        with open(input_filename, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_filename} not found. Create it first!")
        return

    print(f"Starting pipeline: Processing {len(events)} events...")

    tagged_results = []

    for event in events:
        print(f"Stitching tags for: {event['title']}...")
        
        # Get the tags (using AI)
        tags = generate_tags(event, use_ai=True)
        
        # Add the tags to the event dictionary
        event['tags'] = tags
        tagged_results.append(event)

    # Save the newly enriched data to a new file
    with open(output_filename, 'w') as f:
        json.dump(tagged_results, f, indent=2)

    print(f"Success! Enriched data saved to {output_filename}")

# --- EXECUTION ---
if __name__ == "__main__":
    # This runs the whole process
    process_events_pipeline('server/sample_events.json', 'server/tagged_events.json')