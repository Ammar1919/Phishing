"use client";
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [loading, setLoading] = useState(false);

  const handleSignUp = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:1800/gmail/authorize");
      const data = await res.json();
      console.log(data)
      if (data.auth_url) {
        window.location.href = data.auth_url;
      } else {
        alert("Failed to get authorization URL.");
      }
    } catch (err) {
      alert("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-white to-blue-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors">
      <div className="bg-white/90 dark:bg-gray-900/90 shadow-2xl rounded-3xl p-10 w-full max-w-md flex flex-col items-center border border-blue-100 dark:border-gray-800 backdrop-blur-md">
        <div className="mb-6 flex flex-col items-center">
          <svg
            className="w-16 h-16 mb-2 text-blue-600 dark:text-blue-400"
            fill="none"
            viewBox="0 0 48 48"
            stroke="currentColor"
          >
            <rect x="6" y="12" width="36" height="24" rx="4" fill="currentColor" opacity="0.1" />
            <path
              d="M8 14l16 13L40 14"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
            />
            <rect x="6" y="12" width="36" height="24" rx="4" stroke="currentColor" strokeWidth="2" />
          </svg>
          <h1 className="text-3xl font-extrabold mb-2 text-gray-900 dark:text-white tracking-tight">
            Phishing Protection
          </h1>
          <span className="text-blue-600 dark:text-blue-400 font-semibold text-sm tracking-wide uppercase">
            Secure Gmail Sign Up
          </span>
        </div>
        <p className="mb-8 text-gray-600 dark:text-gray-300 text-center">
          Protect your inbox from phishing. Sign up securely with your Gmail account—no email or password required.
        </p>
        <button
          onClick={handleSignUp}
          disabled={loading}
          className="w-full py-3 px-6 rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white font-bold text-lg shadow-lg transition-all duration-200 disabled:opacity-60 flex items-center justify-center"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Redirecting...
            </>
          ) : (
            <>
              <svg className="h-5 w-5 mr-2" viewBox="0 0 48 48" fill="none">
                <rect x="6" y="12" width="36" height="24" rx="4" fill="#fff" />
                <path
                  d="M8 14l16 13L40 14"
                  stroke="#4285F4"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  fill="none"
                />
                <rect x="6" y="12" width="36" height="24" rx="4" stroke="#4285F4" strokeWidth="2" />
              </svg>
              Sign Up with Gmail
            </>
          )}
        </button>
      </div>
      <footer className="mt-12 text-gray-400 text-xs text-center">
        &copy; {new Date().getFullYear()} Phishing Protection. All rights reserved.
      </footer>
    </div>
  );
}
