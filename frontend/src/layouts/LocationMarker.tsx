import { useEffect, useState } from "react";
import { Marker, Popup, useMap } from "react-leaflet";

export default function LocationMarker() {
  const [position, setPosition] = useState<[number, number] | null>(null);
  const map = useMap();

  useEffect(() => {
    map.locate({
      setView: true,
      maxZoom: 17,
      enableHighAccuracy: true,
      timeout: 10000,
    });

    map.on("locationfound", (e) => {
      console.log("Accuracy:", e.accuracy);

      setPosition([
        e.latlng.lat,
        e.latlng.lng,
      ]);
    });

    map.on("locationerror", (e) => {
      console.log("Location error:", e.message);
    });

    return () => {
      map.off("locationfound");
      map.off("locationerror");
    };
  }, [map]);

  return position ? (
    <Marker position={position}>
      <Popup>
        Your location
      </Popup>
    </Marker>
  ) : null;
}