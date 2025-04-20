"use client";

import { useState } from "react";

export default function SignUp() {
  const [selectedRole, setSelectedRole] = useState("Admin");
  const [formData, setFormData] = useState({
    nameOrCompany: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  interface OAuthResponse {
    url: string;
  }

  const handleOAuthSignIn = async (provider: string): Promise<void> => {
    try {
      const response = await fetch(`/api/auth/${provider}`, {
        method: "GET",
        credentials: "include", // adjust if your API uses cookies
      });

      if (response.ok) {
        const { url }: OAuthResponse = await response.json(); // Expecting { url: "..." } from backend
        window.location.href = url;
      } else {
        console.error(`OAuth login with ${provider} failed`);
      }
    } catch (error) {
      console.error("Error during OAuth login:", error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  interface GeneralPayload {
    fullName: string;
    email: string;
    password: string;
    confirmPassword: string;
    role: string;
  }

  interface CompanyPayload {
    companyName: string;
    email: string;
    password: string;
    confirmPassword: string;
    role: string;
  }

  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();

    // Adjust payload based on role
    const payload: GeneralPayload | CompanyPayload =
      selectedRole === "General"
        ? {
            fullName: formData.nameOrCompany,
            email: formData.email,
            password: formData.password,
            confirmPassword: formData.confirmPassword,
            role: selectedRole,
          }
        : {
            companyName: formData.nameOrCompany,
            email: formData.email,
            password: formData.password,
            confirmPassword: formData.confirmPassword,
            role: selectedRole,
          };

    try {
      const response = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        alert("Account created successfully!");
        // navigate or redirect here if needed
      } else {
        const error = await response.json();
        console.error("Signup failed:", error);
        alert(error.message || "Signup failed");
      }
    } catch (err) {
      console.error("Error submitting signup form:", err);
      alert("An unexpected error occurred!");
    }
  };

  return (
    <div className="flex h-screen">
      {/* Left Panel */}
      <div className="w-1/2 bg-gradient-to-b from-[#E7D9FB] to-[#F0E9FF] flex flex-col justify-center items-center">
        <h1 className="text-5xl font-extrabold text-[#6D4AFF] mb-6 tracking-wide">
          atlas
        </h1>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">
          Get Started with Us
        </h2>
        <p className="text-sm text-gray-700 mb-6 text-center w-3/4">
          Complete these easy steps to register your account
        </p>

        <div className="space-y-4 w-[70%]">
          {["Admin", "General", "Employee"].map((role, index) => (
            <button
              key={role}
              onClick={() => setSelectedRole(role)}
              className={`flex items-center justify-between w-full py-3 px-4 rounded-lg font-medium text-sm transform transition-transform duration-200 ease-in-out
        ${
          selectedRole === role
            ? "bg-[#7864E8] text-white"
            : "bg-[#E9E4FF] text-[#7864E8]"
        }
        hover:scale-105 hover:shadow-lg active:scale-95`}
            >
              <span className="bg-white text-[#7864E8] rounded-full px-2 py-0.5 text-xs font-bold mr-3">
                {index + 1}
              </span>
              Sign Up as {role}
              <span />
            </button>
          ))}
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-1/2 flex items-center justify-center bg-white px-8">
        <div className="w-full max-w-md">
          <h2 className="text-xl font-semibold text-center mb-6 text-black cursor-pointer">
            Sign Up Account
          </h2>

          {/* OAuth Buttons */}
          <div className="flex justify-center space-x-4 mb-4">
            <button
              onClick={() => handleOAuthSignIn("google")}
              className="border px-6 py-2 rounded-lg flex items-center space-x-2 text-sm cursor-pointer 
               transform transition-transform duration-200 ease-in-out hover:scale-105 hover:shadow-lg"
            >
              <img
                src="https://www.svgrepo.com/show/475656/google-color.svg"
                alt="Google"
                className="w-5 h-5"
              />
              <span className="text-black">Google</span>
            </button>

            <button
              onClick={() => handleOAuthSignIn("linkedin")}
              className="border px-6 py-2 rounded-lg flex items-center space-x-2 text-sm cursor-pointer 
               transform transition-transform duration-200 ease-in-out hover:scale-105 hover:shadow-lg"
            >
              <img
                src="https://www.svgrepo.com/show/448234/linkedin.svg"
                alt="LinkedIn"
                className="w-5 h-5"
              />
              <span className="text-black">LinkedIn</span>
            </button>
          </div>

          {/* Divider */}
          <div className="flex items-center justify-center mb-6">
            <div className="h-px bg-gray-300 w-1/3" />
            <span className="mx-2 text-sm text-black">Or</span>
            <div className="h-px bg-gray-300 w-1/3" />
          </div>

          {/* Form Fields */}
          <form onSubmit={handleFormSubmit}>
            <div className="mb-4">
              <label className="block text-sm mb-1 text-black">
                {selectedRole === "General" ? "Full Name" : "Company Name"}
              </label>
              <input
                type="text"
                name="nameOrCompany"
                placeholder={
                  selectedRole === "General"
                    ? "Enter Full Name"
                    : "Enter Company Name"
                }
                value={formData.nameOrCompany}
                onChange={handleInputChange}
                className="w-full px-4 py-2 rounded-md bg-gray-100 text-sm text-black"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm mb-1 text-black">Email</label>
              <input
                type="email"
                name="email"
                placeholder="Enter Email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-2 rounded-md bg-gray-100 text-sm text-black"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm mb-1 text-black">Password</label>
              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleInputChange}
                className="w-full px-4 py-2 rounded-md bg-gray-100 text-sm text-black"
                required
              />
            </div>

            <div className="mb-2">
              <label className="block text-sm mb-1 text-black">
                Confirm Password
              </label>
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm your password"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="w-full px-4 py-2 rounded-md bg-gray-100 text-black"
                required
              />
              <p className="text-xs text-black mt-1">
                Must be at least 8 characters.
              </p>
            </div>

            <button
              type="submit"
              className="w-full bg-[#7864E8] text-white py-3 rounded-lg font-semibold mt-4
             transform transition-transform duration-200 ease-in-out 
             hover:scale-105 hover:shadow-lg active:scale-95"
            >
              Sign up
            </button>
          </form>

          <p className="text-sm text-center mt-6 text-black">
            Already have an account?{" "}
            <a href="/login" className="text-[#7864E8] font-medium">
              Log In
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
