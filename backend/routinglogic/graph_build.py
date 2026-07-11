"""
Builds the graph the routing engine searches over.

Two kinds of directed edges, matching Section 8.2 of the spec:

  RIDE edge   : two consecutive stops on the same trip.
                weight = scheduled travel time between them, in minutes.
  TRANSFER edge: two DIFFERENT stops within walking distance of each other.
                weight = estimated walking time, in minutes, plus a small
                fixed buffer so the router never assumes an instant
                teleport between buses.

We use a MultiDiGraph (not a plain DiGraph) because two different bus
routes can connect the exact same pair of stops -- we want to keep both
options available, not silently overwrite one with the other.

This module builds the graph ONCE at import time and exposes it as
`GRAPH`. Rebuild it (call build_graph() again) whenever the GTFS feed is
re-imported -- see Section 8.7 of the spec doc ("rebuilt on every
import, never patched in place").
"""

import networkx as nx
from routinglogic.load import stops, trips, stop_times
from routinglogic.nearest import _tree, _stop_ids, _project  # reuse the same KD-tree machinery

WALK_SPEED_M_PER_MIN = 80          # ~4.8 km/h, a comfortable walking pace
TRANSFER_RADIUS_M = 400            # only offer a transfer within this distance
TRANSFER_BUFFER_MIN = 2            # minimum time assumed to physically change buses


def _parse_gtfs_time_to_minutes(t):
    """
    GTFS allows times past 24:00:00 (a trip that starts one day and
    technically "ends" the next, e.g. 25:10:00). This parses HH:MM:SS
    into plain minutes-since-midnight, handling that overflow correctly
    instead of crashing on it.
    """
    h, m, s = t.split(":")
    return int(h) * 60 + int(m) + int(s) / 60


def _add_ride_edges(G):
    """One edge per consecutive stop pair within each trip."""
    # Sorting once up front is much faster than sorting inside a per-trip loop.
    st = stop_times.sort_values(["trip_id", "stop_sequence"])
    trip_route = trips.set_index("trip_id")["route_id"].to_dict()

    for trip_id, group in st.groupby("trip_id"):
        route_id = trip_route.get(trip_id)
        rows = list(group.itertuples())
        for a, b in zip(rows, rows[1:]):
            dep = _parse_gtfs_time_to_minutes(a.departure_time)
            arr = _parse_gtfs_time_to_minutes(b.arrival_time)
            duration = max(arr - dep, 0.5)  # guard against bad/zero-length data
            G.add_edge(
                a.stop_id, b.stop_id,
                key=f"ride:{trip_id}:{a.stop_sequence}",
                kind="ride",
                route_id=route_id,
                trip_id=trip_id,
                duration_min=duration,
            )


def _add_transfer_edges(G):
    """
    One (two-way) edge between any two DIFFERENT stops within
    TRANSFER_RADIUS_M of each other, using the same KD-tree built for
    nearest-stop lookup so we don't build a second spatial index.
    """
    for i, stop_id in enumerate(_stop_ids):
        nearby_idx = _tree.query_ball_point(_tree.data[i], r=TRANSFER_RADIUS_M)
        for j in nearby_idx:
            if j == i:
                continue
            other_id = _stop_ids[j]
            dist_m = ((_tree.data[i][0] - _tree.data[j][0]) ** 2 +
                      (_tree.data[i][1] - _tree.data[j][1]) ** 2) ** 0.5
            walk_min = dist_m / WALK_SPEED_M_PER_MIN + TRANSFER_BUFFER_MIN
            G.add_edge(
                stop_id, other_id,
                key="transfer",
                kind="transfer",
                duration_min=walk_min,
                distance_m=round(dist_m, 1),
            )


def build_graph():
    G = nx.MultiDiGraph()
    for row in stops.itertuples():
        G.add_node(row.stop_id, stop_name=row.stop_name, lat=row.stop_lat, lon=row.stop_lon)
    _add_ride_edges(G)
    _add_transfer_edges(G)
    return G


# Built once, at import time. Call build_graph() again after a GTFS re-import.
GRAPH = build_graph()