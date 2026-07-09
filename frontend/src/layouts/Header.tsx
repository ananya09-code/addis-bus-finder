import Logo from "./Logo"
import DesktopNav from "./DesktopNav"
import MobileNav from "./MobileNav"
import { useIsMobile } from "../hook/useisMobile"
import { useState } from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars} from "@fortawesome/free-solid-svg-icons";
function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const isMobile = useIsMobile();

    return (
        <header className="bg-red-500">
            {isMobile ? (
                <>
                    <div className="flex justify-between items-center p-1 border-b-2 border-white">
                        <Logo />

                        <button
                            aria-label="Toggle navigation menu"
                            className="bg-red text-white shadow-md  min-w-6 max-h-6 rounded-1xl hover:bg-red-400 "
                            onClick={() => setIsMenuOpen(prev => !prev)}
                        >
                            <FontAwesomeIcon icon={faBars} />
                        </button>
                    </div>

                    {isMenuOpen && <MobileNav />}
                </>
            ) : (
                <div className="flex justify-between">
                    <Logo />
                    <DesktopNav />
                </div>
            )}
        </header>
    );
}
export default Header;