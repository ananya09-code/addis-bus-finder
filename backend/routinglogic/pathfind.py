"""
Multi-leg routing WITH transfers -- used only when direct.py finds
nothing. Runs a weighted shortest-path search over the graph built in
graph_build.py and turns the resulting node path back into readable
legs (ride / transfer), the same shape the frontend/map already expects
from direct.py.

--- How ambiguous start/end names are handled ---
A search for "Megenagna" can match many physical stop_ids (see
resolve.py). Rather than guessing one, we add a temporary "virtual"
start node wired to every candidate with a free (zero-cost) edge, and
same for the end. Dijkstra then naturally finds the best real start/end
combination on its own. The virtual nodes are removed again right after
the search -- they never persist in the shared graph.

--- How "objective" changes the search ---
fastest          : edge weight = travel/walk time only
fewest_transfers : edge weight = travel/walk time + a fixed penalty
                   every time a transfer (walking) edge is used
(There's no real fare data in this feed yet -- see Section 10 of the
spec doc for the fare table this would need. "cheapest" is not
implemented until that data exists.)
"""

import networkx as nx
from routinglogic.graph_build import GRAPH

TRANSFER_PENALTY_MIN = 15  # only affects ranking for "fewest_transfers", not real time


def _weight_fn(objective):
    """Returns a function networkx calls for every edge (handles parallel edges)."""
    def weight(u, v, parallel_edges):
        best = None
        for data in parallel_edges.values():
            w = data["duration_min"]
            if objective == "fewest_transfers" and data["kind"] == "transfer":
                w += TRANSFER_PENALTY_MIN
            if best is None or w < best:
                best = w
        return best
    return weight


def _cheapest_parallel_edge(u, v, objective):
    """Same rule as _weight_fn, but returns the winning edge's DATA, not just its weight."""
    best_data, best_w = None, None
    for data in GRAPH[u][v].values():
        w = data["duration_min"]
        if objective == "fewest_transfers" and data["kind"] == "transfer":
            w += TRANSFER_PENALTY_MIN
        if best_w is None or w < best_w:
            best_w, best_data = w, data
    return best_data


def plan_with_transfers(start_candidates, end_candidates, objective="fastest"):
    """
    start_candidates / end_candidates: lists of dicts from resolve_location(...)["candidates"]
    objective: "fastest" or "fewest_transfers"

    Returns a list with 0 or 1 itinerary dict (same shape as direct.py's
    output, but with 1+ "ride" legs separated by "transfer" legs).
    """
    start_ids = [c["stop_id"] for c in start_candidates]
    end_ids = [c["stop_id"] for c in end_candidates]

    V_START, V_END = "__virtual_start__", "__virtual_end__"
    GRAPH.add_node(V_START)
    GRAPH.add_node(V_END)
    for sid in start_ids:
        GRAPH.add_edge(V_START, sid, key="virtual", kind="virtual", duration_min=0)
    for eid in end_ids:
        GRAPH.add_edge(eid, V_END, key="virtual", kind="virtual", duration_min=0)

    try:
        path = nx.dijkstra_path(GRAPH, V_START, V_END, weight=_weight_fn(objective))
    except nx.NetworkXNoPath:
        return []
    finally:
        # Always clean up the virtual nodes, even if the search raised or found nothing --
        # otherwise they'd leak into every future query on this shared graph.
        GRAPH.remove_node(V_START)
        GRAPH.remove_node(V_END)

    real_path = path[1:-1]  # drop the virtual start/end nodes
    if len(real_path) < 2:
        return []

    return [_build_itinerary(real_path, objective)]


def _build_itinerary(node_path, objective):
    """Turns a plain list of stop_ids into grouped ride/transfer legs with full stop detail."""
    legs = []
    current_ride = None
    total_time = 0.0

    for u, v in zip(node_path, node_path[1:]):
        edge = _cheapest_parallel_edge(u, v, objective)
        total_time += edge["duration_min"]
        u_info = _stop_info(u)
        v_info = _stop_info(v)

        if edge["kind"] == "ride":
            if current_ride and current_ride["route_id"] == edge["route_id"]:
                current_ride["stops"].append(v_info)
            else:
                if current_ride:
                    _finalize_ride_leg(current_ride)
                    legs.append(current_ride)
                current_ride = {
                    "type": "ride",
                    "route_id": edge["route_id"],
                    "trip_id": edge["trip_id"],
                    "stops": [u_info, v_info],
                }
        else:  # transfer edge
            if current_ride:
                _finalize_ride_leg(current_ride)
                legs.append(current_ride)
                current_ride = None
            legs.append({
                "type": "transfer",
                "from_stop": u_info,
                "to_stop": v_info,
                "duration_min": round(edge["duration_min"], 1),
                "distance_m": edge.get("distance_m"),
            })

    if current_ride:
        _finalize_ride_leg(current_ride)
        legs.append(current_ride)

    transfer_count = sum(1 for l in legs if l["type"] == "transfer")
    return {"total_time_min": round(total_time, 1), "transfers": transfer_count, "legs": legs}


def _finalize_ride_leg(ride_leg):
    """Attaches route names, board/alight summary, and stop_count to a grouped ride leg."""
    from routinglogic.load import routes_by_id
    route_row = routes_by_id.loc[ride_leg["route_id"]]
    ride_leg["route_short_name"] = str(route_row["route_short_name"])
    ride_leg["route_long_name"] = str(route_row["route_long_name"])
    ride_leg["board_stop"] = ride_leg["stops"][0]
    ride_leg["alight_stop"] = ride_leg["stops"][-1]
    ride_leg["stop_count"] = len(ride_leg["stops"])


def _stop_info(stop_id):
    from routinglogic.load import stops_by_id
    row = stops_by_id.loc[stop_id]
    return {"stop_id": stop_id, "stop_name": row["stop_name"], "lat": float(row["stop_lat"]), "lon": float(row["stop_lon"])}