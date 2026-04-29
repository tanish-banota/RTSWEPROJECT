import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytz
from dateutil import parser as dateutil_parser

# Adding data_pipeline folder to search path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

EASTERN = pytz.timezone("America/New_York")
WEEKDAYS = ["monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"]

_MARKDOWN_RE = re.compile(r"\*{1,2}|_{1,2}|~~|`+|^> ?", re.MULTILINE)

_ISO_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_SLASH_DATE_RE = re.compile(r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b")
_MONTH_DATE_RE = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?\b",
    re.IGNORECASE,
)
_WEEKDAY_RE = re.compile(
    r"\b((?:this|next)\s+)?(" + "|".join(WEEKDAYS) + r")\b",
    re.IGNORECASE,
)

# Matches ranges like "7pm - 9pm", "7:00pm to 9:00pm", "7–9pm"
_TIME_RANGE_RE = re.compile(
    r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm))\s*(?:[-–]|to)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b",
    re.IGNORECASE,
)
_TIME_RE = re.compile(r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b", re.IGNORECASE)

_LOCATION_RE = re.compile(
    r"(?:location|venue|room|where|held at|held in|place)[:\s]+([^\n,\.]{3,60})",
    re.IGNORECASE,
)


def strip_markdown(text: str) -> str:
    return _MARKDOWN_RE.sub("", text).strip()


def extract_title(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:120]
    return "Untitled Event"


def _resolve_weekday(modifier: str, day_name: str, reference: datetime) -> datetime:
    target_wd = WEEKDAYS.index(day_name.lower())
    current_wd = reference.weekday()
    days_ahead = (target_wd - current_wd) % 7 or 7
    if modifier and "next" in modifier.lower():
        days_ahead += 7
    return reference + timedelta(days=days_ahead)


def extract_date(text: str, reference: datetime) -> datetime | None:
    for pattern in (_ISO_DATE_RE, _SLASH_DATE_RE, _MONTH_DATE_RE):
        m = pattern.search(text)
        if m:
            try:
                return dateutil_parser.parse(m.group(), default=reference)
            except ValueError:
                pass

    m = _WEEKDAY_RE.search(text)
    if m:
        return _resolve_weekday(m.group(1) or "", m.group(2), reference)

    return None


def _parse_time(time_str: str, date: datetime) -> datetime:
    dt = dateutil_parser.parse(time_str, default=date)
    return date.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)


def extract_times(text: str, date: datetime):
    """Returns (start_utc, end_utc). end_utc is None if no range found."""
    m = _TIME_RANGE_RE.search(text)
    if m:
        try:
            start = EASTERN.localize(_parse_time(
                m.group(1), date)).astimezone(timezone.utc)
            end = EASTERN.localize(_parse_time(
                m.group(2), date)).astimezone(timezone.utc)
            return start, end
        except Exception:
            pass

    m = _TIME_RE.search(text)
    if m:
        try:
            start = EASTERN.localize(_parse_time(
                m.group(1), date)).astimezone(timezone.utc)
            return start, None
        except Exception:
            pass

    return None, None


def extract_location(text: str) -> str:
    m = _LOCATION_RE.search(text)
    return m.group(1).strip() if m else ""


def parse_discord_messages(raw_data=None):
    from config import DISCORD_RAW_PATH, DISCORD_CLEAN_PATH

    if raw_data is None:
        try:
            with open(DISCORD_RAW_PATH, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            print(
                f"Error: discord raw data not found at {DISCORD_RAW_PATH}. Run discord_fetcher first.")
            return None

    clean_events = []
    skipped = 0

    for msg in raw_data:
        try:
            content = msg.get("content", "")
            if not content.strip():
                skipped += 1
                continue

            # Naive reference datetime derived from message timestamp for relative day resolution
            reference = dateutil_parser.parse(
                msg["timestamp"]).replace(tzinfo=None)
            clean_text = strip_markdown(content)

            date_dt = extract_date(clean_text, reference)
            if date_dt is None:
                skipped += 1
                continue

            start_utc, end_utc = extract_times(clean_text, date_dt)

            if start_utc is None:
                start_utc = EASTERN.localize(
                    date_dt.replace(hour=0, minute=0, second=0, microsecond=0)
                ).astimezone(timezone.utc)

            clean_events.append({
                "title": extract_title(clean_text),
                "club_name": msg.get("author", {}).get("username", ""),
                "description": clean_text,
                "location": extract_location(clean_text),
                "date": date_dt.strftime("%Y-%m-%d"),
                "start_time": start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end_time": end_utc.strftime("%Y-%m-%dT%H:%M:%SZ") if end_utc else "",
                "source": "discord",
            })
        except Exception as e:
            print(f"Skipping a message due to parsing error: {e}")
            skipped += 1
            continue

    DISCORD_CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DISCORD_CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_events, f, indent=4)

    print(
        f"Successfully parsed {len(clean_events)} Discord events! ({skipped} messages skipped)")
    return clean_events


if __name__ == "__main__":
    parse_discord_messages()
