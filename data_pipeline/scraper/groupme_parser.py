import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from dateutil import parser as dateutil_parser

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
_TIME_RANGE_RE = re.compile(
    r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm))\s*(?:[-–]|to)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b",
    re.IGNORECASE,
)
_TIME_RE = re.compile(r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b", re.IGNORECASE)
_LOCATION_RE = re.compile(
    r"(?:location|venue|room|where|held at|held in|place)[:\s]+([^\n,\.]{3,60})",
    re.IGNORECASE,
)

# Matches edit-log messages like "Username edited to: ..."
_EDIT_LOG_RE = re.compile(r"^.+\s+edited\s+to:\s*", re.IGNORECASE)


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
    """Returns (start_et, end_et). end_et is None if no range found."""
    m = _TIME_RANGE_RE.search(text)
    if m:
        try:
            start = EASTERN.localize(_parse_time(m.group(1), date))
            end = EASTERN.localize(_parse_time(m.group(2), date))
            return start, end
        except Exception:
            pass

    m = _TIME_RE.search(text)
    if m:
        try:
            start = EASTERN.localize(_parse_time(m.group(1), date))
            return start, None
        except Exception:
            pass

    return None, None


def extract_location(text: str) -> str:
    m = _LOCATION_RE.search(text)
    return m.group(1).strip() if m else ""


def parse_groupme_messages(raw_data=None):
    from config import GROUPME_RAW_PATH, GROUPME_CLEAN_PATH

    if raw_data is None:
        try:
            with open(GROUPME_RAW_PATH, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            print(
                f"Error: GroupMe raw data not found at {GROUPME_RAW_PATH}. Run groupme_fetcher first.")
            return None

    clean_events = []
    skipped = 0

    for msg in raw_data:
        try:
            text = msg.get("text") or ""
            if not text.strip() or _EDIT_LOG_RE.match(text):
                skipped += 1
                continue

            # Convert Unix timestamp to Eastern so relative day resolution (e.g. "this Thursday") uses the correct local date
            reference = datetime.fromtimestamp(msg["created_at"], tz=EASTERN).replace(tzinfo=None)
            clean_text = strip_markdown(text)

            date_dt = extract_date(clean_text, reference)
            if date_dt is None:
                skipped += 1
                continue

            start_et, end_et = extract_times(clean_text, date_dt)

            if start_et is None:
                start_et = EASTERN.localize(
                    date_dt.replace(hour=0, minute=0, second=0, microsecond=0)
                )

            clean_events.append({
                "title": extract_title(clean_text),
                "club_name": msg.get("name", ""),
                "description": clean_text,
                "location": extract_location(clean_text),
                "date": date_dt.strftime("%Y-%m-%d"),
                "start_time": start_et.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_time": end_et.strftime("%Y-%m-%dT%H:%M:%S") if end_et else "",
                "source": "groupme",
            })
        except Exception as e:
            print(f"Skipping a message due to parsing error: {e}")
            skipped += 1
            continue

    GROUPME_CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GROUPME_CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_events, f, indent=4)

    print(f"Successfully parsed {len(clean_events)} GroupMe events! ({skipped} messages skipped)")
    return clean_events


if __name__ == "__main__":
    parse_groupme_messages()
