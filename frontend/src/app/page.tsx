"use client";

/**
 * Landing / Onboarding page — first page users see.
 * Beautiful hero with animated elements, linked feature cards, and dark mode toggle.
 */

import { useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Heart, BookOpen, MessageCircle, Shield, Sun, Moon, Brain, Layers } from "lucide-react";
import { useUIStore, useToast } from "@/lib/stores";

const features = [
  {
    icon: MessageCircle,
    title: "AI Health Companion",
    description: "Chat with Saheli about health topics in your language",
    color: "from-dusty-rose-400 to-warm-peach-400",
    href: "/chat",
  },
  {
    icon: BookOpen,
    title: "Visual Learning",
    description: "Interactive lessons on health, hygiene, and nutrition",
    color: "from-lavender-400 to-dusty-rose-300",
    href: "/learn",
  },
  {
    icon: Brain,
    title: "Quiz & Test",
    description: "Test your health knowledge and earn points",
    color: "from-sage-400 to-sage-500",
    href: "/quiz",
  },
  {
    icon: Layers,
    title: "Flashcards",
    description: "Quick-flip cards to memorize health facts",
    color: "from-warm-peach-400 to-warm-peach-500",
    href: "/flashcards",
  },
];

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

export default function LandingPage() {
  const { theme, toggleTheme, setTheme } = useUIStore();
  const toast = useToast();

  // Apply persisted theme on mount
  useEffect(() => {
    setTheme(theme);
  }, []);

  return (
    <div className="min-h-screen overflow-hidden">
      {/* Decorative Background */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -right-32 -top-32 h-80 w-80 rounded-full bg-dusty-rose-200/30 blur-3xl" />
        <div className="absolute -left-20 top-1/3 h-60 w-60 rounded-full bg-lavender-200/30 blur-3xl" />
        <div className="absolute bottom-20 right-10 h-40 w-40 rounded-full bg-warm-peach-200/30 blur-3xl" />
        <div className="absolute -bottom-10 left-1/4 h-52 w-52 rounded-full bg-sage-200/20 blur-3xl" />
      </div>

      {/* Top Bar with Dark Mode Toggle */}
      <motion.header
        className="sticky top-0 z-50 border-b border-dusty-rose-100/50 dark:border-gray-700/50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md transition-colors"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="flex h-14 items-center justify-between px-4 mx-auto max-w-lg">
          <div className="flex items-center gap-2">
            <span className="text-xl">🌸</span>
            <span className="bg-gradient-to-r from-dusty-rose-500 to-lavender-500 bg-clip-text text-lg font-bold text-transparent">
              Sehat Saheli
            </span>
          </div>
          <button
            onClick={() => {
              toggleTheme();
              toast.info(theme === "dark" ? "Light mode ☀️" : "Dark mode 🌙");
            }}
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
      </motion.header>

      {/* Content */}
      <div className="relative mx-auto max-w-lg px-6 py-10">
        {/* Hero Section */}
        <motion.div
          className="mb-12 text-center"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <motion.div
            className="mx-auto mb-6 flex h-24 w-24 items-center justify-center rounded-3xl bg-gradient-to-br from-dusty-rose-400 to-warm-peach-400 shadow-lg shadow-dusty-rose-200"
            animate={{ rotate: [0, 5, -5, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
          >
            <span className="text-5xl">🌸</span>
          </motion.div>

          <h1 className="mb-3 text-4xl font-bold">
            <span className="bg-gradient-to-r from-dusty-rose-500 via-lavender-500 to-sage-500 bg-clip-text text-transparent">
              Sehat Saheli
            </span>
          </h1>
          <p className="text-lg text-gray-500 dark:text-gray-400 font-medium">
            Your Health Companion 💜
          </p>
          <p className="mt-3 text-sm text-gray-400 dark:text-gray-500 leading-relaxed max-w-xs mx-auto">
            Learn about your body with a friendly AI assistant that speaks your language.
            Safe, private, and always here for you.
          </p>
        </motion.div>

        {/* Feature Cards — Linked */}
        <div className="mb-10 grid grid-cols-2 gap-3">
          {features.map((feature, index) => (
            <Link key={feature.title} href={feature.href}>
              <motion.div
                variants={fadeInUp}
                initial="initial"
                animate="animate"
                transition={{ delay: 0.2 + index * 0.1, duration: 0.5 }}
                className="group rounded-2xl border border-white/60 dark:border-gray-700 bg-white/70 dark:bg-gray-800/70 p-4 backdrop-blur-sm shadow-sm transition-all duration-300 hover:shadow-md hover:scale-[1.02] cursor-pointer h-full"
              >
                <div
                  className={`mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-r ${feature.color} shadow-sm transition-transform duration-300 group-hover:scale-110`}
                >
                  <feature.icon className="h-5 w-5 text-white" />
                </div>
                <h3 className="mb-1 text-sm font-semibold text-gray-800 dark:text-gray-100 group-hover:text-dusty-rose-600 dark:group-hover:text-dusty-rose-300 transition-colors">{feature.title}</h3>
                <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{feature.description}</p>
              </motion.div>
            </Link>
          ))}
        </div>

        {/* CTA Buttons */}
        <motion.div
          className="space-y-3"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.5 }}
        >
          <Link href="/quiz" className="block">
            <Button className="w-full h-13 text-base font-semibold bg-gradient-to-r from-dusty-rose-400 to-warm-peach-400 shadow-lg shadow-dusty-rose-200/50 hover:shadow-xl transition-all">
              Start Learning 🌺
            </Button>
          </Link>
          <Link href="/login" className="block">
            <Button variant="outline" className="w-full h-12 text-sm font-medium border-dusty-rose-200 dark:border-dusty-rose-700 text-dusty-rose-600 dark:text-dusty-rose-300 hover:bg-dusty-rose-50 dark:hover:bg-dusty-rose-900/20">
              I already have an account
            </Button>
          </Link>
        </motion.div>

        {/* Language Support Badge */}
        <motion.p
          className="mt-8 text-center text-xs text-gray-400"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.5 }}
        >
          Available in: English • हिन्दी • মাংলা • தமிழ் • తెలుగు • ಕನ್ನಡ • मराठी • ગુજરાતી
        </motion.p>
      </div>
    </div>
  );
}
