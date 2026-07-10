from routinglogic.load import stops, routes, trips, stop_times


def find_buse(start, end):
    # Find starting and ending stops
    start_stops = stops[
        stops["stop_name"].str.contains(start, case=False, na=False)
    ]

    end_stops = stops[
        stops["stop_name"].str.contains(end, case=False, na=False)
    ]

    if start_stops.empty:
        return {
            "success": False,
            "message": f"Start stop '{start}' not found",
            "data": []
        }

    if end_stops.empty:
        return {
            "success": False,
            "message": f"End stop '{end}' not found",
            "data": []
        }


    start_ids = start_stops["stop_id"].tolist()
    end_ids = end_stops["stop_id"].tolist()


    # Find trips that pass through start stop
    trips_to_start = stop_times[
        stop_times["stop_id"].isin(start_ids)
    ]["trip_id"].unique()


    # Find trips that also pass through end stop
    possible_trips = stop_times[
        (stop_times["trip_id"].isin(trips_to_start)) &
        (stop_times["stop_id"].isin(end_ids))
    ]["trip_id"].unique()


    if len(possible_trips) == 0:
        return {
            "success": False,
            "message": "There is no direct route",
            "data": []
        }


    good_trips = []


    # Check direction
    for trip in possible_trips:

        this_trip = stop_times[
            stop_times["trip_id"] == trip
        ]

        start_sequence = this_trip[
            this_trip["stop_id"].isin(start_ids)
        ]["stop_sequence"].min()


        end_sequence = this_trip[
            this_trip["stop_id"].isin(end_ids)
        ]["stop_sequence"].min()


        if start_sequence < end_sequence:
            good_trips.append(trip)



    if not good_trips:
        return {
            "success": False,
            "message": "Buses found, but they travel in the opposite direction",
            "data": []
        }


    print("Good trips found:", good_trips)


    results = []


    for trip in good_trips:

        trip_row = trips[
            trips["trip_id"] == trip
        ]


        if not trip_row.empty:

            route_id = trip_row["route_id"].iloc[0]


            route_row = routes[
                routes["route_id"] == route_id
            ]


            if not route_row.empty:

                results.append({
                    "route_short_name": str(
                        route_row["route_short_name"].iloc[0]
                    ),

                    "route_long_name": str(
                        route_row["route_long_name"].iloc[0]
                    ),

                    "trip_id": int(trip)
                })


    if not results:
        return {
            "success": False,
            "message": "No usable routes found",
            "data": []
        }


    return {
        "success": True,
        "message": "Routes found",
        "data": results
    }