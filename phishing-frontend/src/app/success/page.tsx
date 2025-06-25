import '../globals.css';

export default function SuccessPage() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-white to-blue-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors">
            <div className="bg-white/90 dark:bg-gray-900/90 shadow-2xl rounded-3xl p-10 w-full max-w-md flex flex-col items-center border border-blue-100 dark:border-gray-800 backdrop-blur-md">
                <div className="mb-6 flex flex-col items-center">
                    <svg
                        className="w-16 h-16 mb-2 text-green-600 dark:text-green-400"
                        fill="none"
                        viewBox="0 0 48 48"
                        stroke="currentColor"
                    >
                        <circle cx="24" cy="24" r="22" stroke="currentColor" strokeWidth="4" fill="currentColor" opacity="0.1" />
                        <path
                            d="M16 24l6 6 10-10"
                            stroke="currentColor"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            fill="none"
                        />
                    </svg>
                    <h1 className="text-3xl font-extrabold mb-2 text-gray-900 dark:text-white tracking-tight">
                        Success!
                    </h1>
                    <span className="text-green-600 dark:text-green-400 font-semibold text-sm tracking-wide uppercase">
                        Gmail Connected
                    </span>
                </div>
                <p className="mb-8 text-gray-600 dark:text-gray-300 text-center">
                    Your Gmail account has been connected successfully.<br />
                    You can now leave this page.
                </p>
            </div>
            <footer className="mt-12 text-gray-400 text-xs text-center">
                &copy; {new Date().getFullYear()} Phishing Protection. All rights reserved.
            </footer>
        </div>
    );
}