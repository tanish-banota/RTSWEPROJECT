import os
import json
import time
from google import genai
from dotenv import load_dotenv
from tqdm import tqdm 

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CURRENT_MODEL = "gemini-2.5-flash" 

def generate_tags(event, use_ai=True, attempt=1):
    title = event.get('title', 'No Title')
    description = event.get('description', '')
    club = event.get('club_name', 'Unknown Club')
    MAX_ATTEMPTS = 3
        
    if not use_ai:
        return ["general", "campus life"]

    prompt = f"Categorize this Rutgers event: {club} | {title} | {description}. Return 3-5 comma-separated tags."
    
    try:
        # Small delay to respect free-tier limits
        time.sleep(0.8) 

        response = client.models.generate_content(model=CURRENT_MODEL, contents=prompt)
        if not response.text:
            raise ValueError("Empty response from AI")
            
        return [t.strip().lower() for t in response.text.split(",")]

    except Exception as e:
        error_str = str(e).upper()
        # Handle the slowdowns/503s specifically
        if ("503" in error_str or "UNAVAILABLE" in error_str or "429" in error_str) and attempt <= MAX_ATTEMPTS:
            wait_time = attempt * 5
            # Use tqdm.write so the print doesn't break the progress bar UI
            tqdm.write(f"⚠️  SLOWDOWN: Google is busy. Retrying '{title}' in {wait_time}s... (Attempt {attempt})")
            time.sleep(wait_time)
            return generate_tags(event, use_ai=True, attempt=attempt + 1)
        
        tqdm.write(f"❌ AI ERROR for '{title}': {e}")
        return generate_tags(event, use_ai=False)


def process_events_pipeline(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        new_events = json.load(f)

    existing_tags = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            try:
                existing_tags = json.load(f)
            except:
                existing_tags = []

    already_processed = {f"{e.get('title')}-{e.get('date')}" for e in existing_tags}
    
    # Filter for brand new events
    to_process = [e for e in new_events if f"{e.get('title')}-{e.get('date')}" not in already_processed]
    
    print(f"--- Pipeline Started ---")
    print(f"Found {len(new_events)} total events.")
    print(f"Skipping {len(new_events) - len(to_process)} already tagged events.")
    print(f"Processing {len(to_process)} new events...\n")

    # The Progress Bar with a "Detailed" loop
    for event in tqdm(to_process, desc="Tagging Progress", unit="event", leave=True):
        tqdm.write(f"✨ Processing: {event.get('title')}") # This prints above the bar
        
        tags = generate_tags(event, use_ai=True)
        event['tags'] = tags
        
        existing_tags.append(event)
        
        # Save after every event so we don't lose data if it crashes
        with open(output_file, 'w') as f:
            json.dump(existing_tags, f, indent=4)

    print(f"\n✅ Pipeline Complete! Check '{output_file}' for results.")

if __name__ == "__main__":
    process_events_pipeline('data/clean/clean.json', 'server/tagged_events.json')