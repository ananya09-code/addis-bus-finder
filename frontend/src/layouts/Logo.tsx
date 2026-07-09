import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBus } from "@fortawesome/free-solid-svg-icons";

function Logo(){
    return <span className="text-white font-bold p-4 hover:text-red-100">
        <FontAwesomeIcon icon={faBus} />
          አቋራጭ Bus Finder
          </span>
}
export default Logo;