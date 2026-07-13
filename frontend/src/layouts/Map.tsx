import { MapContainer, TileLayer,Polyline,Popup,Marker } from "react-leaflet";
import type { LatLngBoundsExpression } from "leaflet";

import FitRoute from "../hook/Fitroute";
const addisBounds: LatLngBoundsExpression = [
  [8.80, 38.55], // Southwest corner
  [9.15, 39.00], // Northeast corner
];


export default function Map({data}:any) {
    const points = data?.[0]?.geometry;
    const stops = data?.[0]?.stops;



  return (
<MapContainer
  center={[8.9806, 38.7578]}
  zoom={13}
  minZoom={11}
  maxZoom={18}
  maxBounds={addisBounds}
  maxBoundsViscosity={1.0}
  className="h-125 w-full rounded-lg"
>
  <TileLayer
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attribution="© OpenStreetMap contributors"
  />



  {points && (
    <>
      <Polyline
        positions={points}
        pathOptions={{
          weight: 5
        }}
      />

      <FitRoute points={points} />
    </>
  )}

  {stops?.map((stop:any) => (
    <Marker
      key={stop.stop_id}
      position={[stop.lat, stop.lon]}
    >
      <Popup>
        {stop.stop_name}
      </Popup>
    </Marker>
  ))}

</MapContainer>
  );
}