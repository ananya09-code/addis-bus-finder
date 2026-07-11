"""
Finds DIRECT routes (no transfer needed) between a set of candidate
start stops and a set of candidate end stops.

This is the fast path: checked first, before we ever touch the full
graph/Dijkstra machinery in pathfind.py. Most short trips in a real
city are not direct, but when one is, it's the simplest and cheapest
answer to compute -- no point running a full graph search for it.
"""

from routinglogic.load import stops, routes, trips, stop_times


def find_direct_routes(start_candidates, end_candidates):
    """
    start_candidates / end_candidates: lists of dicts as returned by
    resolve.resolve_location(...)["candidates"]

    Returns a list of itinerary dicts (empty list if no direct route
    exists). Each itinerary has exactly one "ride" leg.
    """
    start_ids = {c["stop_id"] for c in start_candidates}
    end_ids = {c["stop_id"] for c in end_candidates}

    if start_ids & end_ids:
        return []  # same physical stop given as both ends -- not a trip

    trips_to_start = stop_times[stop_times["stop_id"].isin(start_ids)]["trip_id"].unique()
    possible_trips = stop_times[
        (stop_times["trip_id"].isin(trips_to_start)) & (stop_times["stop_id"].isin(end_ids))
    ]["trip_id"].unique()

    results = []
    seen = set()

    for trip_id in possible_trips:
        this_trip = stop_times[stop_times["trip_id"] == trip_id].sort_values("stop_sequence")
        start_rows = this_trip[this_trip["stop_id"].isin(start_ids)]
        end_rows = this_trip[this_trip["stop_id"].isin(end_ids)]

        board_seq = start_rows["stop_sequence"].min()
        board_stop_id = start_rows.loc[start_rows["stop_sequence"].idxmin(), "stop_id"]
        alight_seq = end_rows["stop_sequence"].min()
        alight_stop_id = end_rows.loc[end_rows["stop_sequence"].idxmin(), "stop_id"]

        if board_seq >= alight_seq:
            continue  # this trip runs the wrong way for this start/end pair

        trip_row = trips[trips["trip_id"] == trip_id]
        if trip_row.empty:
            continue
        route_id = trip_row["route_id"].iloc[0]
        route_row = routes[routes["route_id"] == route_id]
        if route_row.empty:
            continue

        dedup_key = (route_id, board_stop_id, alight_stop_id)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        leg = this_trip[
            (this_trip["stop_sequence"] >= board_seq) & (this_trip["stop_sequence"] <= alight_seq)
        ].merge(stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]], on="stop_id", how="left")

        stop_list = [
            {"stop_id": r.stop_id, "stop_name": r.stop_name, "lat": float(r.stop_lat), "lon": float(r.stop_lon)}
            for r in leg.itertuples()
        ]

        results.append({
            "total_time_min": round(_ride_duration(this_trip, board_seq, alight_seq), 1),
            "transfers": 0,
            "legs": [{
                "type": "ride",
                "route_id": route_id,
                "route_short_name": str(route_row["route_short_name"].iloc[0]),
                "route_long_name": str(route_row["route_long_name"].iloc[0]),
                "trip_id": str(trip_id),
                "board_stop": stop_list[0],
                "alight_stop": stop_list[-1],
                "stop_count": len(stop_list),
                "stops": stop_list,
            }],
        })

    return results


def _ride_duration(trip_stop_times, board_seq, alight_seq):
    """Sum of scheduled travel time (minutes) between board_seq and alight_seq on one trip."""
    from routinglogic.graph_build import _parse_gtfs_time_to_minutes
    board_row = trip_stop_times[trip_stop_times["stop_sequence"] == board_seq].iloc[0]
    alight_row = trip_stop_times[trip_stop_times["stop_sequence"] == alight_seq].iloc[0]
    return _parse_gtfs_time_to_minutes(alight_row["arrival_time"]) - _parse_gtfs_time_to_minutes(board_row["departure_time"])