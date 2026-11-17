"""Stage 2: add a `date` column (YYYY-MM-DD) taken from `timestamp`."""
import sys
from pathlib import Path

import pandas as pd


def main(src: str, dst: str) -> None:
    df = pd.read_csv(src, dtype={"duration_seconds": int})
    df["date"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d")
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dst, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
