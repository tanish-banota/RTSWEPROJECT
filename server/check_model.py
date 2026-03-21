import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- Available Models ---")
# The new SDK returns objects that we can convert to dictionaries to see all fields
for model in client.models.list():
    # .name is still there, but let's see what else it has
    print(f"ID: {model.name}")
    # This will show you the ACTUAL field names available in 2026
    # print(model.model_dump()) # Uncomment this if you want to see everything