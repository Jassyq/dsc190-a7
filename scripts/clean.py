"""Stage 1: clean the raw events.

Drops rows with missing fields, invalid event_type, or non-positive
duration_seconds, and normalizes timestamp to YYYY-MM-DDTHH:MM:SS.
"""
import sys
from pathlib import Path

import pandas as pd

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}
TIMESTAMP_FORMATS = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S"]


def parse_timestamp(value: str):
    """Parse one of the known timestamp formats (fractional seconds dropped)."""
    value = value.strip()
    if "." in value:  # e.g. 2026-04-28T00:51:56.561
        value = value.split(".")[0]
    for fmt in TIMESTAMP_FORMATS:
        try:
            return pd.to_datetime(value, format=fmt)
        except ValueError:
            continue
    return pd.NaT


def main(src: str, dst: str) -> None:
    df = pd.read_csv(src, dtype=str, keep_default_na=False)
    df = df.apply(lambda col: col.str.strip())

    # Missing fields
    df = df[(df != "").all(axis=1)]

    # Invalid event_type
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    # Non-positive / non-numeric duration (kept as a whole number)
    duration = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[duration > 0].copy()
    df["duration_seconds"] = duration[df.index].round().astype(int)

    # Normalize timestamps to ISO 8601; drop anything unparseable
    ts = df["timestamp"].map(parse_timestamp)
    df = df[ts.notna()].copy()
    df["timestamp"] = pd.to_datetime(ts[df.index]).dt.strftime("%Y-%m-%dT%H:%M:%S")

    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dst, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
