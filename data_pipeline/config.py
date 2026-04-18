from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
RAW_PATH = PIPELINE_DIR / "data" / "raw" / "raw.json"
CLEAN_PATH = PIPELINE_DIR / "data" / "clean" / "clean.json"
