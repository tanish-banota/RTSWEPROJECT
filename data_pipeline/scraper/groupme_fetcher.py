import os
import json
import sys
import time
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GROUPME_API_BASE = "https://api.groupme.com/v3"
MESSAGES_PER_REQUEST = 25


def _get_token():
    token = os.getenv("GROUPME_ACCESS_TOKEN")
    if not token:
        raise EnvironmentError(
            "GROUPME_ACCESS_TOKEN is not set. Add it to data_pipeline/.env"
        )
    return token


def _get_group_ids():
    raw = os.getenv("GROUPME_GROUP_IDS", "")
    ids = [gid.strip() for gid in raw.split(",") if gid.strip()]
    if not ids:
        raise EnvironmentError(
            "GROUPME_GROUP_IDS is not set. Add a comma-separated list to data_pipeline/.env"
        )
    return ids


def _get(url: str, params: dict) -> requests.Response:
    response = requests.get(url, params=params)
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 2))
        time.sleep(retry_after)
        response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def _find_events_channel(group_id: str, token: str) -> str | None:
    """Returns the channel_id of the 'Events' topic if one exists, else None."""
    try:
        resp = _get(
            f"{GROUPME_API_BASE}/groups/{group_id}/channels", {"token": token})
        channels = resp.json().get("response", {}).get("channels", [])
        for ch in channels:
            if ch.get("display_name", "").strip().lower() == "events":
                return ch["id"]
    except requests.exceptions.HTTPError:
        pass
    return None


def fetch_group_messages(group_id: str, token: str) -> list:
    events_channel_id = _find_events_channel(group_id, token)

    if events_channel_id:
        print(
            f"  Found Events topic in group {group_id}, fetching from channel instead of main chat...")
        url = f"{GROUPME_API_BASE}/channels/{events_channel_id}/messages"
    else:
        url = f"{GROUPME_API_BASE}/groups/{group_id}/messages"

    resp = _get(url, {"token": token, "limit": MESSAGES_PER_REQUEST})
    return resp.json().get("response", {}).get("messages", [])


def fetch_groupme_announcements():
    from config import GROUPME_RAW_PATH
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    token = _get_token()
    group_ids = _get_group_ids()

    print(f"Fetching GroupMe messages from {len(group_ids)} group(s)...")

    all_messages = []
    failed_groups = []

    for group_id in group_ids:
        try:
            print(f"  Fetching group {group_id}...")
            group_resp = _get(f"{GROUPME_API_BASE}/groups/{group_id}", {"token": token})
            group_name = group_resp.json().get("response", {}).get("name", group_id)
            messages = fetch_group_messages(group_id, token)
            for msg in messages:
                msg["_group_id"] = group_id
                msg["_group_name"] = group_name
            all_messages.extend(messages)
            print(f"  Fetched {len(messages)} messages from group {group_id}.")
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP error on group {group_id}: {e}")
            failed_groups.append(group_id)
        except requests.exceptions.RequestException as e:
            print(f"  Request error on group {group_id}: {e}")
            failed_groups.append(group_id)

    if failed_groups:
        print(
            f"Warning: failed to fetch {len(failed_groups)} group(s): {failed_groups}")

    if not all_messages:
        print("No GroupMe messages fetched.")
        return None

    GROUPME_RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GROUPME_RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, indent=4)

    print(
        f"Success! {len(all_messages)} raw GroupMe messages saved to {GROUPME_RAW_PATH}")
    return all_messages


if __name__ == "__main__":
    fetch_groupme_announcements()
