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
        return generate_tags(event, use_ai=False)

def process_events_pipeline(input_file, output_file):
    # 1. Load the new raw events
    with open(input_file, 'r') as f:
        new_events = json.load(f)

    # 2. Load existing tagged events so we don't repeat work
    existing_tags = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_tags = json.load(f)

    # Create a "lookup set" of titles we've already tagged
    already_processed = {f"{e['title']}-{e['date']}" for e in existing_tags}

    final_output = existing_tags # Start with what we already have
    newly_tagged_count = 0

    print(f"Checking {len(new_events)} events...")

    for event in new_events:
        event_key = f"{event['title']}-{event['date']}"
        
        if event_key in already_processed:
            print(f"⏭️  Already tagged: {event['title']}")
            continue

        # 3. Only run the AI for truly NEW events
        print(f"✨ Tagging NEW event: {event['title']}...")
        tags = generate_tags(event, use_ai=True)
        event['tags'] = tags
        
        final_output.append(event)
        newly_tagged_count += 1

    # 4. Save the combined list back to the file
    with open(output_file, 'w') as f:
        json.dump(final_output, f, indent=4)

    print(f"\nPipeline complete! Added {newly_tagged_count} new tagged events.")

# --- EXECUTION ---
if __name__ == "__main__":
    # This runs the whole process
    #process_events_pipeline('server/sample_events.json', 'server/tagged_events.json')
    process_events_pipeline('data/clean/clean.json', 'server/tagged_events.json')