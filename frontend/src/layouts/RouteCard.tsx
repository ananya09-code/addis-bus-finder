import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBus } from "@fortawesome/free-solid-svg-icons";

type RouteCardProps = {
  busNum: string;
  start: string;
  end: string;
};

function RouteCard({ busNum, start, end }: RouteCardProps) {
  return (
    <div className="flex flex-col gap-3 rounded-xl bg-white p-4 shadow-md">
      {/* Bus Number */}
      <div className="flex items-center gap-2 text-lg font-bold text-red-600">
        <FontAwesomeIcon icon={faBus} />
        <span>Bus {busNum}</span>
      </div>

      {/* Route */}
      <div className="flex items-center justify-between  rounded-lg bg-gray-50 p-3 text-sm">
        <div className="font-medium text-gray-800">
          {start}
        </div>

        <span className="px-3 text-xl text-gray-400">
          ⟷
        </span>

        <div className="font-medium text-gray-800">
          {end}
        </div>
      </div>
    </div>
  );
}

export default RouteCard;