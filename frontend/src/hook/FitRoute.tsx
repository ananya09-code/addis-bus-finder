import { useMap } from "react-leaflet";
import { useEffect } from "react";

function FitRoute({ points }: { points: any }) {
  const map = useMap();

  useEffect(() => {
    if (points && points.length > 0) {
      map.fitBounds(points);
    }
  }, [points, map]);

  return null;
}

export default FitRoute;