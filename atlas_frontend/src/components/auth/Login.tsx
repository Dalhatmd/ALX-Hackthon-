"use client";

import { useState } from "react";

export default function Login() {
  const [selectedRole, setSelectedRole] = useState("Admin");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
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

  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();

    const payload = {
      email: formData.email,
      password: formData.password,
      role: selectedRole,
    };

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        alert("Login successful!");
        // navigate or redirect here if needed
      } else {
        const error = await response.json();
        console.error("Login failed:", error);
        alert(error.message || "Login failed");
      }
    } catch (err) {
      console.error("Error submitting login form:", err);
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
          Welcome Back!
        </h2>
        <p className="text-sm text-gray-700 mb-6 text-center w-3/4">
          Please sign in to continue
        </p>

        <div className="space-y-4 w-[70%]">
          {["Admin", "General", "Employee"].map((role, index) => (
            <button
              key={role}
              onClick={() => setSelectedRole(role)}
              className={`flex items-center justify-between w-full py-3 px-4 rounded-lg font-medium text-sm transform transition-transform duration-200 ease-in-out
        ${selectedRole === role
                  ? "bg-[#7864E8] text-white"
                  : "bg-[#E9E4FF] text-[#7864E8]"}
        hover:scale-105 hover:shadow-lg active:scale-95`}
            >
              <span className="bg-white text-[#7864E8] rounded-full px-2 py-0.5 text-xs font-bold mr-3">
                {index + 1}
              </span>
              Sign In as {role}
              <span />
            </button>
          ))}
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-1/2 flex items-center justify-center bg-white px-8">
        <div className="w-full max-w-md">
          <h2 className="text-xl font-semibold text-center mb-6 text-black cursor-pointer">
            Sign In to Your Account
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

            <button
              type="submit"
              className="w-full bg-[#7864E8] text-white py-3 rounded-lg font-semibold mt-4
             transform transition-transform duration-200 ease-in-out 
             hover:scale-105 hover:shadow-lg active:scale-95"
            >
              Sign In
            </button>
          </form>

          <p className="text-sm text-center mt-6 text-black">
            Don't have an account?{" "}
            <a href="/signup" className="text-[#7864E8] font-medium">
              Sign Up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
