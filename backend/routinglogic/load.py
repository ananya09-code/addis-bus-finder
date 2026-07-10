from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "et-addisababa"


def _load_gtfs_table(file_name: str):
    file_path = DATA_DIR / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"GTFS file not found: {file_path}")
    return pd.read_csv(file_path)


routes = _load_gtfs_table("routes.txt")
stops = _load_gtfs_table("stops.txt")
trips = _load_gtfs_table("trips.txt")
stop_times = _load_gtfs_table("stop_times.txt")

__all__ = ["routes", "stops", "trips", "stop_times"]
