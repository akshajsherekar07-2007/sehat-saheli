"use client";

/**
 * Top header bar with app name, language selector, and dark mode toggle.
 */

import { useEffect } from "react";
import { Globe, Sun, Moon } from "lucide-react";
import { useUIStore } from "@/lib/stores";
import { SUPPORTED_LANGUAGES } from "@/lib/constants";
import type { LanguageCode } from "@/types";

export function TopBar() {
  const { language, setLanguage, theme, toggleTheme, setTheme } = useUIStore();

  // Apply persisted theme on mount
  useEffect(() => {
    setTheme(theme);
  }, []);

  return (
    <header className="sticky top-0 z-50 border-b border-dusty-rose-100 dark:border-gray-700 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md transition-colors">
      <div className="flex h-14 items-center justify-between px-4">
        {/* App branding — left */}
        <div className="flex items-center gap-2">
          <span className="text-xl">🌸</span>
          <h1 className="bg-gradient-to-r from-dusty-rose-500 to-lavender-500 bg-clip-text text-lg font-bold text-transparent">
            Sehat Saheli
          </h1>
        </div>

        {/* Controls — right */}
        <div className="flex items-center gap-3">
          {/* Language selector */}
          <div className="flex items-center gap-1">
            <Globe className="h-4 w-4 text-gray-400" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as LanguageCode)}
              className="appearance-none bg-transparent text-sm font-medium text-gray-600 dark:text-gray-300 focus:outline-none cursor-pointer pr-1"
              aria-label="Select language"
            >
              {SUPPORTED_LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.nativeName}
                </option>
              ))}
            </select>
          </div>

          {/* Dark mode toggle — extreme right */}
          <button
            onClick={toggleTheme}
            className="flex h-9 w-9 items-center justify-center rounded-full border border-gray-200 dark:border-gray-600 text-gray-500 dark:text-yellow-400 hover:bg-dusty-rose-50 dark:hover:bg-gray-700 transition-colors"
            aria-label="Toggle dark mode"
          >
            {theme === "dark" ? (
              <Sun className="h-[18px] w-[18px]" />
            ) : (
              <Moon className="h-[18px] w-[18px]" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
