# RTSWEPROJECT
# 🛡️ Rutgers Club Recommender (RTSWE Project)

Welcome to the backend! This repository contains the scraper logic and the server API.

## 🚀 Getting Started (For Team Members)

Follow these steps to sync your local environment with the project setup.

### 1. Clone and Open
Open this folder in **VSCode**.

### 2. Set up the Virtual Environment
Open your terminal in VSCode (`Ctrl + ~`) and run:
```bash
# Create the environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
.\venv\Scripts\activate

#Install dependencies
pip install -r requirements.txt

# If you add new dependencies, run this command again to update requirements.txt
pip freeze > requirements.txt

#Create a .env file in root directory and add the following keys (check the google doc for keys)
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here

#Run the tagging engine by adding raw data into: server/sample_events.json
#Run the engine to generate server/tagged_events.json file:
python server/tagging_engine.py

#Upload the tagged events to Supabase:
python server/upload_to_supabase.py