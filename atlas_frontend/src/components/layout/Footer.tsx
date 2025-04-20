import { FaLinkedinIn, FaInstagram } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";

export default function Footer() {
  return (
    <footer className="bg-white shadow-sm py-10 px-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Left: Logo + Copyright */}
        <div className="flex items-center gap-2 text-sm text-gray-800">
          <span className="text-2xl font-bold text-indigo-600 tracking-wider">
            ATLAS
          </span>
          <span className="text-sm text-gray-600">© Atlas 2025</span>
        </div>

        {/* Center: Links */}
        <div className="flex items-center gap-6 text-sm text-gray-800">
          <a href="#" className="hover:underline">
            Security
          </a>
          <a href="#" className="hover:underline">
            Blog
          </a>
          <a href="#" className="hover:underline">
            Privacy Policy
          </a>
        </div>

        {/* Right: Socials */}
        <div className="flex items-center gap-4 text-xl text-gray-800">
          <a href="#" aria-label="LinkedIn">
            <FaLinkedinIn />
          </a>
          <a href="#" aria-label="Instagram">
            <FaInstagram />
          </a>
          <a href="#" aria-label="X / Twitter">
            <FaXTwitter />
          </a>
        </div>
      </div>
    </footer>
  );
}
