from datetime import date
from re import MULTILINE, Match, Pattern, compile

MONTHS: dict[str, int] = {
    "Jan": 1,
    "Fev": 2,
    "Mar": 3,
    "Avr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Auo": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

def get_events(text: str) -> list[dict[str, str]]:
    # Get date
    date_pattern: Pattern[str] = compile(r"(?P<month>[A-Za-zéû]+)\.?(?P<day>\d{2})-(?P<year>\d{4})\s+\[EST\]")
    date_match: Match[str] | None = date_pattern.search(text)

    if not date_match:
        raise ValueError("Date not found.")

    month = date_match.group("month").rstrip(".")
    day = int(date_match.group("day"))
    year = int(date_match.group("year"))
    date_: str = date(year, MONTHS[month], day).isoformat()

    # Get time
    events_text: str = text[date_match.end():]
    event_pattern: Pattern[str] = compile(r"^\d{2}:\d{2}\.\d{2}\s+.+$", MULTILINE)
    lines: list[str] = event_pattern.findall(events_text)
    line: str
    events = []
    
    for line in lines:
        time_raw: str
        event: str
        time_raw, event = line.split(maxsplit=1)
        time: str = time_raw.replace(".", ":")
        events.append({"datetime": f"{date_} {time}", "event": event.strip()})

    return events
