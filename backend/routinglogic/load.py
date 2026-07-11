"""
Loads the raw GTFS .txt files into pandas DataFrames.

Everything is read as `dtype=str` on purpose: stop_id/trip_id/route_id in
this feed are things like "node/7037183574" or plain numeric strings like
"12" -- mixing types causes silent join failures later (a string "12"
will not match an int 12). Keep IDs as strings everywhere in this codebase.

Numeric columns we actually need to do math on (stop_sequence, lat/lon,
headway_secs) are converted explicitly below, right after loading.
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "data", "gtfs_raw")

stops = pd.read_csv(os.path.join(BASE, "stops.txt"), dtype=str)
routes = pd.read_csv(os.path.join(BASE, "routes.txt"), dtype=str)
trips = pd.read_csv(os.path.join(BASE, "trips.txt"), dtype=str)
stop_times = pd.read_csv(os.path.join(BASE, "stop_times.txt"), dtype=str)
frequencies = pd.read_csv(os.path.join(BASE, "frequencies.txt"), dtype=str)

# --- numeric conversions -----------------------------------------------
stop_times["stop_sequence"] = stop_times["stop_sequence"].astype(int)
stops["stop_lat"] = stops["stop_lat"].astype(float)
stops["stop_lon"] = stops["stop_lon"].astype(float)
frequencies["headway_secs"] = frequencies["headway_secs"].astype(int)

# --- quick lookup indexes, built once at import time --------------------
# Reused everywhere instead of re-filtering the big DataFrames every call.
stops_by_id = stops.set_index("stop_id", drop=False)
routes_by_id = routes.set_index("route_id", drop=False)
trips_by_id = trips.set_index("trip_id", drop=False)