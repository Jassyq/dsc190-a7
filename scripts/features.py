"""Stage 3: add `duration_minutes` and `weekday` columns."""
import sys
from pathlib import Path

import pandas as pd


def main(src: str, dst: str) -> None:
    df = pd.read_csv(src, dtype={"duration_seconds": int})
    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dst, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
