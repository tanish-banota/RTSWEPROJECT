from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_DIR.parent
RAW_PATH = PIPELINE_DIR / "data" / "raw" / "raw.json"
CLEAN_PATH = PIPELINE_DIR / "data" / "clean" / "clean.json"
TAGGED_PATH = PROJECT_ROOT / "server" / "tagged_events.json"
DISCORD_RAW_PATH = PIPELINE_DIR / "data" / "raw" / "discord_raw.json"
DISCORD_CLEAN_PATH = PIPELINE_DIR / "data" / "clean" / "discord_clean.json"
GROUPME_RAW_PATH = PIPELINE_DIR / "data" / "raw" / "groupme_raw.json"
GROUPME_CLEAN_PATH = PIPELINE_DIR / "data" / "clean" / "groupme_clean.json"
