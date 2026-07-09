import { Link } from "react-router-dom";
function DesktopNav() {

  return (
     <nav className="text-black">
      <ul className="flex items-center gap-30 p-4">
        <li className="hover:text-white">
          <Link to="/">Home</Link>
        </li>

        <li className="hover:text-white">
          <Link to="/routes">Routes</Link>
        </li>

        <li className="hover:text-white">
          <Link to="/about">About</Link>
        </li>
      </ul>
    </nav>)
 
}

export default DesktopNav;