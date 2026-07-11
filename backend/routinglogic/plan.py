"""
THE FUNCTION YOUR BACKEND CALLS. Everything else in this package is a
supporting piece for this one entry point.

    from routinglogic.plan import plan_trip
    result = plan_trip("Megenagna", "Legedadi")
    result = plan_trip((9.02, 38.80), "Piassa")       # coordinate start is fine too
    result = plan_trip("Megenagna", "Legedadi", objective="fewest_transfers")

What it does, in order:
  1. Resolve start/end input (text name OR (lat, lon)) to candidate stops.
  2. Try a DIRECT route first (direct.py) -- cheap and simple, most
     specific answer when one exists.
  3. If no direct route exists, fall back to the full graph search WITH
     transfers (pathfind.py).
  4. Return one consistent JSON-ready shape either way, so your backend
     (and the frontend map) never has to care which path was taken
     internally.
"""

from routinglogic.resolve import resolve_location
from routinglogic.direct import find_direct_routes
from routinglogic.pathfind import plan_with_transfers

VALID_OBJECTIVES = ("fastest", "fewest_transfers")


def plan_trip(start, end, objective="fastest"):
    """
    start, end : place name string OR (lat, lon) tuple
    objective  : "fastest" (default) or "fewest_transfers"

    Returns:
    {
        "success": bool,
        "message": str,
        "objective": str,
        "origin_candidates": [...],       # every physical stop the start text/point matched
        "destination_candidates": [...],
        "direct": bool,                   # True if the chosen itinerary needs no transfer
        "itineraries": [ ... ]            # see direct.py / pathfind.py for the leg shape
    }
    """
    if objective not in VALID_OBJECTIVES:
        return _error(f"objective must be one of {VALID_OBJECTIVES}")

    origin = resolve_location(start)
    if not origin["success"]:
        return _error(origin["message"])

    destination = resolve_location(end)
    if not destination["success"]:
        return _error(destination["message"])

    # --- Step 1: try direct (no transfer) first ---------------------------
    direct_itineraries = find_direct_routes(origin["candidates"], destination["candidates"])
    if direct_itineraries:
        direct_itineraries.sort(key=lambda it: it["total_time_min"])
        return {
            "success": True,
            "message": "Direct route found",
            "objective": objective,
            "origin_candidates": origin["candidates"],
            "destination_candidates": destination["candidates"],
            "direct": True,
            "itineraries": direct_itineraries,
        }

    # --- Step 2: fall back to multi-leg routing with transfers ------------
    transfer_itineraries = plan_with_transfers(origin["candidates"], destination["candidates"], objective)
    if transfer_itineraries:
        return {
            "success": True,
            "message": "Route found with transfer(s)",
            "objective": objective,
            "origin_candidates": origin["candidates"],
            "destination_candidates": destination["candidates"],
            "direct": False,
            "itineraries": transfer_itineraries,
        }

    return {
        "success": False,
        "message": "No route found, even with transfers, within the current transfer radius",
        "objective": objective,
        "origin_candidates": origin["candidates"],
        "destination_candidates": destination["candidates"],
        "direct": False,
        "itineraries": [],
    }


def _error(message):
    return {
        "success": False, "message": message, "objective": None,
        "origin_candidates": [], "destination_candidates": [], "direct": False, "itineraries": [],
    }