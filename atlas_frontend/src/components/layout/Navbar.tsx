"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import Link from 'next/link';

export default function Navbar() {
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  interface HandleToggleProps {
    (menuName: string): void;
  }

  const handleToggle: HandleToggleProps = (menuName) => {
    setOpenDropdown((prev) => (prev === menuName ? null : menuName));
  };


  const BulletIcon = () => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M10 18C12.1217 18 14.1566 17.1571 15.6569 15.6569C17.1571 14.1566 18 12.1217 18 10C18 7.87827 17.1571 5.84344 15.6569 4.34315C14.1566 2.84285 12.1217 2 10 2C7.87827 2 5.84344 2.84285 4.34315 4.34315C2.84285 5.84344 2 7.87827 2 10C2 12.1217 2.84285 14.1566 4.34315 15.6569C5.84344 17.1571 7.87827 18 10 18ZM11 7C11 6.73478 10.8946 6.48043 10.7071 6.29289C10.5196 6.10536 10.2652 6 10 6C9.73478 6 9.48043 6.10536 9.29289 6.29289C9.10536 6.48043 9 6.73478 9 7V10.586L7.707 9.293C7.5184 9.11084 7.2658 9.01005 7.0036 9.01233C6.7414 9.0146 6.49059 9.11977 6.30518 9.30518C6.11977 9.49059 6.0146 9.7414 6.01233 10.0036C6.01005 10.2658 6.11084 10.5184 6.293 10.707L9.293 13.707C9.48053 13.8945 9.73484 13.9998 10 13.9998C10.2652 13.9998 10.5195 13.8945 10.707 13.707L13.707 10.707C13.8892 10.5184 13.99 10.2658 13.9877 10.0036C13.9854 9.7414 13.8802 9.49059 13.6948 9.30518C13.5094 9.11977 13.2586 9.0146 12.9964 9.01233C12.7342 9.01005 12.4816 9.11084 12.293 9.293L11 10.586V7Z" fill="#7269F5"/>
    </svg>
  );

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        <Link
          href="/"
          className="text-3xl font-bold text-[#6C63FF] tracking-tight cursor-pointer"
        >
          ATLAS.
        </Link>

        <ul className="flex space-x-6 items-center text-sm font-medium text-gray-700">
          {/* Explore Atlas Dropdown */}
          <li className="relative group">
            <div
              className="flex items-center gap-1 hover:text-black cursor-pointer"
              onClick={() => handleToggle("explore")}
            >
              Explore Atlas <ChevronDown className="w-4 h-4" />
            </div>
            <div
              className={`
              absolute top-full left-0 mt-3 bg-white shadow-xl rounded-lg py-3 text-sm text-gray-700 z-50 
              ${
                openDropdown === "explore"
                  ? "visible opacity-100"
                  : "opacity-0 invisible group-hover:visible group-hover:opacity-100"
              }
              transition-opacity duration-200 grid grid-cols-2 gap-4 p-4 w-[400px]
            `}
            >
              <div>
                <h4 className="px-2 py-1 font-semibold text-gray-500">
                  USE CASES
                </h4>
                <div className="flex flex-col px-2 py-2 hover:bg-gray-50">
                  <a href="#" className="flex items-center gap-2">
                    <BulletIcon />{" "}
                    Desks Booking
                  </a>
                  <span className="text-xs text-gray-500">
                    Easily Book Desk At Youur Workplace
                  </span>
                </div>
                <div className="flex flex-col px-2 py-2 hover:bg-gray-50">
                  <a href="#" className="flex items-center gap-2">
                    <BulletIcon />{" "}
                    Meeting Rooms
                  </a>
                  <span className="text-xs text-gray-500">
                    No More Manual Room Just Seamless Scheduling
                  </span>
                </div>
                <div className="flex flex-col px-2 py-2 hover:bg-gray-50">
                  <a href="#" className="flex items-center gap-2">
                    <BulletIcon />{" "}
                    Event Spaces
                  </a>
                  <span className="text-xs text-gray-500">
                    Forget The Hassle. Book Event Spaces In Seconds, Not Emails
                  </span>
                </div>
                <div className="flex flex-col px-2 py-2 hover:bg-gray-50">
                  <a href="#" className="flex items-center gap-2">
                    <BulletIcon />{" "}
                    Office Spaces
                  </a>
                  <span className="text-xs text-gray-500">
                    Need A Spot To Focus Or Collaborate? Atlas Makes Booking
                    Office Space Quick And Easy
                  </span>
                </div>
              </div>
              <div>
                <h4 className="px-2 py-1 font-semibold text-gray-500">
                  FEATURES
                </h4>
                <a
                  href="#"
                  className="flex items-center gap-2 px-2 py-2 hover:bg-gray-50"
                >
                  <BulletIcon />{" "}
                  Booking System
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 px-2 py-2 hover:bg-gray-50"
                >
                  <BulletIcon />{" "}
                  Notification & Reminders
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 px-2 py-2 hover:bg-gray-50"
                >
                  <BulletIcon />{" "}
                  Reporting & Analytics
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 px-2 py-2 hover:bg-gray-50"
                >
                  <BulletIcon /> User
                  Roles & Access
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 px-2 py-2 hover:bg-gray-50"
                >
                  <BulletIcon /> User
                  Authentication
                </a>
              </div>
            </div>
          </li>

          {/* Solutions Dropdown */}
          <li className="relative group">
            <div
              className="flex items-center gap-1 hover:text-black cursor-pointer"
              onClick={() => handleToggle("solutions")}
            >
              Solutions <ChevronDown className="w-4 h-4" />
            </div>
            <div
              className={`
              absolute top-full left-0 mt-3 w-56 bg-white shadow-xl rounded-lg py-3 text-sm text-gray-700 z-50 
              ${
                openDropdown === "solutions"
                  ? "visible opacity-100"
                  : "opacity-0 invisible group-hover:visible group-hover:opacity-100"
              }
              transition-opacity duration-200 flex flex-col
            `}
            >
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> For
                Companies
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> For
                Learning Institutions
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> For
                Admins
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> User
                Authentication
              </a>
            </div>
          </li>

          {/* Pricing Link */}
          <li>
            <a href="#" className="hover:text-black">
              Pricing
            </a>
          </li>

          {/* Resources Dropdown */}
          <li className="relative group">
            <div
              className="flex items-center gap-1 hover:text-black cursor-pointer"
              onClick={() => handleToggle("resources")}
            >
              Resources <ChevronDown className="w-4 h-4" />
            </div>
            <div
              className={`
              absolute top-full left-0 mt-3 w-56 bg-white shadow-xl rounded-lg py-3 text-sm text-gray-700 z-50 
              ${
                openDropdown === "resources"
                  ? "visible opacity-100"
                  : "opacity-0 invisible group-hover:visible group-hover:opacity-100"
              }
              transition-opacity duration-200 flex flex-col
            `}
            >
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> Help
                Center
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> Blog
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> FAQs
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> Customer
                Service
              </a>
            </div>
          </li>

          {/* About Dropdown */}
          <li className="relative group">
            <div
              className="flex items-center gap-1 hover:text-black cursor-pointer"
              onClick={() => handleToggle("about")}
            >
              About <ChevronDown className="w-4 h-4" />
            </div>
            <div
              className={`
              absolute top-full left-0 mt-3 w-56 bg-white shadow-xl rounded-lg py-3 text-sm text-gray-700 z-50 
              ${
                openDropdown === "about"
                  ? "visible opacity-100"
                  : "opacity-0 invisible group-hover:visible group-hover:opacity-100"
              }
              transition-opacity duration-200 flex flex-col
            `}
            >
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> Our
                story
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> Careers
              </a>
              <a
                href="#"
                className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50"
              >
                <BulletIcon /> Contact
              </a>
            </div>
          </li>

          {/* Log in Link */}
          <li>
            <a href="/login" className="hover:text-black">
              Log in
            </a>
          </li>

          {/* Demo Book Button */}
          <li>
            <button className="bg-[#6C63FF] text-white text-sm font-semibold py-2 px-4 rounded-md hover:bg-[#5A52D4] transition cursor-pointer">
              Demo book
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}
