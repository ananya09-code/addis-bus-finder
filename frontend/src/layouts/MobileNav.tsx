import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome, faInfo, faRoad } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

function MobileNav() {
  return (
    <nav className="text-white">
      <ul className="flex flex-col p-2">
        <li>
          <Link
            to="/"
            className="flex items-center gap-3 rounded-lg p-3 hover:bg-red-600 transition"
          >
            <FontAwesomeIcon icon={faHome} />
            <span>Home</span>
          </Link>
        </li>

        <li>
          <Link
            to="/routes"
            className="flex items-center gap-3 rounded-lg p-3 hover:bg-red-600 transition"
          >
            <FontAwesomeIcon icon={faRoad} />
            <span>Routes</span>
          </Link>
        </li>

        <li>
          <Link
            to="/about"
            className="flex items-center gap-3 rounded-lg p-3 hover:bg-red-600 transition"
          >
            <FontAwesomeIcon icon={faInfo} />
            <span>About</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default MobileNav;