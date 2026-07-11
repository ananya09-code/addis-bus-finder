"""
Turns a raw (lat, lon) coordinate into the nearest bus stop(s).

This is what you call when the frontend sends "user tapped here on the
map" or "use my current location" instead of typed text. It is kept
separate from name-based search (see resolve.py) because the two need
very different logic -- this one is pure geometry.

We build ONE KD-tree at import time (there are ~1,300 stops here, this
costs a few milliseconds) and reuse it for every query rather than
rebuilding it per request.
"""

import math
from scipy.spatial import cKDTree
from routinglogic.load import stops

# Earth radius in meters, used to convert lat/lon degrees to a flat
# approximate plane that's accurate enough at city scale (a few km).
EARTH_RADIUS_M = 6371000

def _project(lat, lon):
    """
    Rough equirectangular projection: turns lat/lon degrees into meters
    on a flat plane, centered near Addis Ababa's latitude (~9 degrees N).
    Good enough for "which stop is nearest" at city scale; NOT accurate
    for long distances or areas far from this latitude band.
    """
    lat_rad = math.radians(lat)
    x = math.radians(lon) * EARTH_RADIUS_M * math.cos(lat_rad)
    y = lat_rad * EARTH_RADIUS_M
    return x, y


# Pre-compute projected coordinates for every stop and build the tree once.
_stop_ids = stops["stop_id"].tolist()
_points = [_project(lat, lon) for lat, lon in zip(stops["stop_lat"], stops["stop_lon"])]
_tree = cKDTree(_points)


def find_nearest_stops(lat, lon, max_results=5, max_radius_m=1000):
    """
    Returns up to `max_results` stops nearest to (lat, lon), sorted by
    walking distance, and never farther than `max_radius_m`.

    Returns: list of dicts, e.g.
      [{"stop_id": "...", "stop_name": "...", "lat":.., "lon":.., "distance_m": 123.4}, ...]
    Empty list if nothing is within range.
    """
    x, y = _project(lat, lon)
    distances, indexes = _tree.query([x, y], k=max_results, distance_upper_bound=max_radius_m)

    # cKDTree returns scalars (not arrays) when max_results == 1 -- normalize to lists.
    if max_results == 1:
        distances, indexes = [distances], [indexes]

    results = []
    for dist, idx in zip(distances, indexes):
        if idx >= len(_stop_ids) or math.isinf(dist):
            continue  # cKDTree pads missing results with inf/out-of-range index
        stop_id = _stop_ids[idx]
        row = stops.loc[stops["stop_id"] == stop_id].iloc[0]
        results.append({
            "stop_id": stop_id,
            "stop_name": row["stop_name"],
            "lat": float(row["stop_lat"]),
            "lon": float(row["stop_lon"]),
            "distance_m": round(float(dist), 1),
        })
    return results