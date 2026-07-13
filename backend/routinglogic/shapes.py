from routinglogic.load import shapes, trips

def get_trip_shape(trip_id):
    trip = trips[trips["trip_id"] == trip_id]

    if trip.empty:
        return []

    shape_id = trip["shape_id"].iloc[0]

    shape = shapes[
        shapes["shape_id"].astype(str) == str(shape_id)
    ].copy()

    shape["shape_pt_sequence"] = (
        shape["shape_pt_sequence"]
        .astype(int)
    )

    shape = shape.sort_values(
        "shape_pt_sequence"
    )

    return [
        [
            float(row.shape_pt_lat),
            float(row.shape_pt_lon)
        ]
        for row in shape.itertuples()
    ]