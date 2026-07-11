"""
Turns whatever the frontend sends -- a typed place name OR a (lat, lon)
pair -- into a list of candidate stop_ids to route from/to.

Why a LIST and not a single stop_id: a name like "Megenagna" matches
24 different physical stop points in this feed (it's a major terminal
with several boarding bays). We don't guess which one the rider means --
we hand every candidate to the routing layer, which is built to accept
multiple start/end candidates at once (see pathfind.py's virtual-node
trick). This keeps resolve.py simple and keeps the "which exact stop did
we actually board at" decision inside the routing logic, where it
belongs.
"""

from routinglogic.load import stops
from routinglogic.nearest import find_nearest_stops


def resolve_location(query, nearest_radius_m=600):
    """
    query: either
      - a string, e.g. "Megenagna"        -> matched by name (substring, case-insensitive)
      - a (lat, lon) tuple, e.g. (9.02, 38.80) -> matched to nearby stops by distance

    Returns: {
        "success": bool,
        "message": str,
        "candidates": [ {stop_id, stop_name, lat, lon}, ... ]
    }
    "candidates" is empty when success is False.
    """
    if isinstance(query, (tuple, list)) and len(query) == 2:
        lat, lon = query
        nearby = find_nearest_stops(lat, lon, max_results=5, max_radius_m=nearest_radius_m)
        if not nearby:
            return {
                "success": False,
                "message": f"No stop found within {nearest_radius_m}m of that location",
                "candidates": [],
            }
        # Only the single closest stop is used for routing from a coordinate --
        # unlike name search, there's no ambiguity to preserve here.
        return {"success": True, "message": "Resolved by location", "candidates": nearby[:1]}

    if isinstance(query, str):
        matches = stops[stops["stop_name"].str.contains(query, case=False, na=False)]
        if matches.empty:
            return {"success": False, "message": f"No stop matching '{query}'", "candidates": []}
        candidates = [
            {
                "stop_id": row.stop_id,
                "stop_name": row.stop_name,
                "lat": float(row.stop_lat),
                "lon": float(row.stop_lon),
            }
            for row in matches.itertuples()
        ]
        return {"success": True, "message": f"{len(candidates)} stop(s) matched", "candidates": candidates}

    return {"success": False, "message": "query must be a place name string or a (lat, lon) tuple", "candidates": []}