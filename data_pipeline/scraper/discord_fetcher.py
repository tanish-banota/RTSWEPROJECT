import os
import json
import sys
import time
import requests
from pathlib import Path

# Adding data_pipeline folder to search path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DISCORD_API_BASE = "https://discord.com/api/v10"

# Limit for Scrapping per request
MESSAGES_PER_REQUEST = 100


def _get_token():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise EnvironmentError(
            "DISCORD_BOT_TOKEN is not set. Add it to data_pipeline/.env"
        )
    return token


def _get_channel_ids():
    """Read channel IDs from DISCORD_CHANNEL_IDS env var (comma-separated)."""
    raw = os.getenv("DISCORD_CHANNEL_IDS", "")
    ids = [cid.strip() for cid in raw.split(",") if cid.strip()]
    if not ids:
        raise EnvironmentError(
            "DISCORD_CHANNEL_IDS is not set. Add a comma-separated list to data_pipeline/.env"
        )
    return ids


def fetch_channel_messages(channel_id: str, headers: dict) -> list:
    """Fetch up to `limit` most recent messages from a single channel."""
    url = f"{DISCORD_API_BASE}/channels/{channel_id}/messages"
    params = {"limit": int(MESSAGES_PER_REQUEST)}

    response = requests.get(url, headers=headers, params=params)

    # 429 = rate limited; back off and retry once
    if response.status_code == 429:
        retry_after = response.json().get("retry_after", 1)
        print(
            f"  Rate limited on channel {channel_id}. Retrying after {retry_after}s...")
        time.sleep(retry_after)
        response = requests.get(url, headers=headers, params=params)

    # To raise errors and prevent crashing
    response.raise_for_status()
    return response.json()


def fetch_discord_announcements():
    from config import DISCORD_RAW_PATH
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    token = _get_token()
    channel_ids = _get_channel_ids()

    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (https://github.com/tanish-banota/RTSWEPROJECT, 1)",
    }

    print(
        f"Fetching Discord announcements from {len(channel_ids)} channel(s)...")

    all_messages = []
    failed_channels = []

    for channel_id in channel_ids:
        try:
            print(f"  Fetching channel {channel_id}...")
            messages = fetch_channel_messages(channel_id, headers)
            # Tag each message with its channel so the parser can use it
            for msg in messages:
                msg["_channel_id"] = channel_id
            all_messages.extend(messages)
            print(
                f"  Fetched {len(messages)} messages from channel {channel_id}.")
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP error on channel {channel_id}: {e}")
            failed_channels.append(channel_id)
        except requests.exceptions.RequestException as e:
            print(f"  Request error on channel {channel_id}: {e}")
            failed_channels.append(channel_id)

    if failed_channels:
        print(
            f"Warning: failed to fetch {len(failed_channels)} channel(s): {failed_channels}")

    if not all_messages:
        print("No Discord messages fetched.")
        return None

    # Check if path exists if not make one
    DISCORD_RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DISCORD_RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, indent=4)

    print(
        f"Success! {len(all_messages)} raw Discord messages saved to {DISCORD_RAW_PATH}")
    return all_messages


if __name__ == "__main__":
    fetch_discord_announcements()
