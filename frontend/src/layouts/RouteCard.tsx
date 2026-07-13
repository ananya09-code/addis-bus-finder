import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBus } from "@fortawesome/free-solid-svg-icons";


type RouteCardProps = {
  busNum: string;
  name:string;
  onselect:boolean;
};

function RouteCard({ busNum, name,onselect }: RouteCardProps) {
 

  return (
    <div className={`flex flex-col gap-3 rounded-xl bg-white p-4 shadow-md ${onselect
      ? "border-2 border-red-600 bg-blue-50 shadow-lg"
      : "border border-gray-300 bg-white hover:shadow-md"}`}
       >
      {/* Bus Number */}
      <div className="flex items-center gap-2 text-lg font-bold text-red-600">
        <FontAwesomeIcon icon={faBus} />
        <span>Bus {busNum}</span>
      </div>

      {/* Route */}
      <div className="flex items-center justify-between  rounded-lg bg-gray-50 p-3 text-sm">
        {name}
      </div>
    </div>
  );
}

export default RouteCard;