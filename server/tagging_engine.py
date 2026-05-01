import os
import json
import time
from google import genai
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CURRENT_MODEL = "gemini-2.0-flash"

_key_exhausted = False

def process_batch(batch, retry_count=0):
    """Sends a group of events to the AI for tagging in one go with retry logic."""
    global _key_exhausted
    MAX_RETRIES = 2
    
    # Create a numbered list for the prompt
    batch_text = ""
    for i, ev in enumerate(batch):
        batch_text += f"{i+1}. {ev.get('club_name')} | {ev.get('title')} | {ev.get('description')[:150]}\n"

    prompt = (
        f"Categorize these {len(batch)} Rutgers events. For each, return exactly 3-5 comma-separated tags. "
        f"Format your response as a numbered list matching the input:\n\n{batch_text}"
    )

    try:
        # Increased base delay to 7 seconds for safer free-tier usage
        time.sleep(7.0) 
        
        response = client.models.generate_content(model=CURRENT_MODEL, contents=prompt)
        
        if not response.text:
            return [["general", "campus life"]] * len(batch)

        lines = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        
        results = []
        for line in lines:
            content = line.split('.', 1)[-1].strip()
            results.append([t.strip().lower() for t in content.split(',')])
        
        while len(results) < len(batch):
            results.append(["general", "campus life"])
            
        return results

    except Exception as e:
        error_msg = str(e).upper()
        # If we hit a rate limit and haven't exceeded retries for this batch
        if ("429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg) and retry_count < MAX_RETRIES:
            tqdm.write(f"🐢 Rate limit hit. Cooling down for 30s before retry {retry_count + 1}...")
            time.sleep(30)
            return process_batch(batch, retry_count=retry_count + 1)
        
        # If we've exhausted retries or hit a different error
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            _key_exhausted = True
            tqdm.write("🚫 Quota exhausted for this run. Switching to fallbacks.")
        else:
            tqdm.write(f"❌ AI Error: {e}")
            
        return [["general", "campus life"]] * len(batch)

def process_events_pipeline(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        incoming_events = json.load(f)

    to_process = []
    for e in incoming_events:
        # Check if tags are missing or are the generic placeholder
        if "campus life" in e.get('tags', []) or not e.get('tags'):
            to_process.append(e)

    if not to_process:
        print("✅ All events already have high-quality tags. Nothing to process.")
        return

    print(f"🚀 Batch processing {len(to_process)} events...")

    batch_size = 5
    for i in tqdm(range(0, len(to_process), batch_size), desc="Batch Progress"):
        if _key_exhausted: 
            break
        
        batch = to_process[i : i + batch_size]
        batch_tags = process_batch(batch)
        
        # Mapping tags back to the original objects
        for j, tags in enumerate(batch_tags):
            batch[j]['tags'] = tags

        # Periodic save so we don't lose progress if it crashes
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(incoming_events, f, indent=4)

    print(f"\n✅ Pipeline finished. Results saved to {output_path}")