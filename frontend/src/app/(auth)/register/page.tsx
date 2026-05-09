"use client";

/**
 * Registration page — collects name, phone, age, address, password, and language.
 */

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { UserPlus, Phone, Lock, User, MapPin, Calendar, Eye, EyeOff, Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { useAuthStore, useUIStore } from "@/lib/stores";
import { SUPPORTED_LANGUAGES } from "@/lib/constants";

export default function RegisterPage() {
  const router = useRouter();
  const { register, isLoading } = useAuthStore();

  const [form, setForm] = useState({
    name: "",
    phone: "",
    age: "",
    address: "",
    password: "",
    preferred_language: "en",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const updateField = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    const age = parseInt(form.age, 10);
    if (isNaN(age) || age < 8 || age > 25) {
      setError("Age must be between 8 and 25");
      return;
    }
    if (form.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    try {
      await register({
        name: form.name,
        phone: form.phone,
        age,
        address: form.address || undefined,
        password: form.password,
        preferred_language: form.preferred_language,
      });
      router.push("/chat");
    } catch (err: any) {
      const msg = err?.response?.data?.message || "Registration failed. Please try again.";
      setError(msg);
    }
  };

  const fields = [
    { id: "name", label: "Full Name", type: "text", icon: User, placeholder: "Enter your name", required: true },
    { id: "phone", label: "Phone Number", type: "tel", icon: Phone, placeholder: "Enter phone number", required: true },
    { id: "age", label: "Age", type: "number", icon: Calendar, placeholder: "Your age", required: true },
    { id: "address", label: "Address (optional)", type: "text", icon: MapPin, placeholder: "Village/Town, District", required: false },
  ];

  const { theme, toggleTheme } = useUIStore();

  return (
    <div className="relative min-h-screen flex items-center justify-center px-6 py-8">
      {/* Dark Mode Toggle */}
      <div className="absolute top-4 right-4 z-50">
        <button
          onClick={toggleTheme}
          className="flex h-10 w-10 items-center justify-center rounded-full bg-white/10 dark:bg-black/10 backdrop-blur-md border border-gray-200/50 dark:border-gray-700/50 text-gray-600 dark:text-yellow-400 hover:bg-white/20 dark:hover:bg-black/20 transition-all shadow-sm"
          aria-label="Toggle dark mode"
        >
          {theme === "dark" ? (
            <Sun className="h-5 w-5" />
          ) : (
            <Moon className="h-5 w-5" />
          )}
        </button>
      </div>

      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -right-20 top-10 h-60 w-60 rounded-full bg-lavender-200/30 blur-3xl" />
        <div className="absolute -left-10 bottom-10 h-50 w-50 rounded-full bg-sage-200/30 blur-3xl" />
      </div>

      <motion.div
        className="relative w-full max-w-sm"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="mb-6 text-center">
          <Link href="/" className="inline-block hover:scale-[1.02] transition-transform">
            <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-lavender-400 to-dusty-rose-400 shadow-lg">
              <span className="text-2xl">🌺</span>
            </div>
            <h1 className="text-2xl font-bold gradient-text">Join Sehat Saheli</h1>
          </Link>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">Start your health awareness journey</p>
        </div>

        <Card className="border-dusty-rose-100/50 dark:border-gray-700 shadow-lg">
          <CardContent className="p-5">
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="rounded-xl bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 px-4 py-3 text-sm text-red-600 dark:text-red-400"
                >
                  {error}
                </motion.div>
              )}

              {fields.map((field) => (
                <div key={field.id} className="space-y-1.5">
                  <Label htmlFor={field.id}>{field.label}</Label>
                  <div className="relative">
                    <field.icon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400 dark:text-gray-500" />
                    <Input
                      id={field.id}
                      type={field.type}
                      placeholder={field.placeholder}
                      value={form[field.id as keyof typeof form]}
                      onChange={(e) => updateField(field.id, e.target.value)}
                      className="pl-10"
                      required={field.required}
                      min={field.type === "number" ? 8 : undefined}
                      max={field.type === "number" ? 25 : undefined}
                    />
                  </div>
                </div>
              ))}

              <div className="space-y-1.5">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400 dark:text-gray-500" />
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Create a password"
                    value={form.password}
                    onChange={(e) => updateField("password", e.target.value)}
                    className="pl-10 pr-10"
                    required
                    minLength={6}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="language">Preferred Language</Label>
                <select
                  id="language"
                  value={form.preferred_language}
                  onChange={(e) => updateField("preferred_language", e.target.value)}
                  className="w-full rounded-xl border-2 border-dusty-rose-200 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-800 dark:text-gray-200 shadow-sm focus:border-dusty-rose-400 focus:outline-none focus:ring-2 focus:ring-dusty-rose-100 dark:focus:ring-dusty-rose-900"
                >
                  {SUPPORTED_LANGUAGES.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.nativeName} ({lang.name})
                    </option>
                  ))}
                </select>
              </div>

              <Button
                type="submit"
                className="w-full h-12 text-base font-semibold bg-gradient-to-r from-lavender-400 to-dusty-rose-400 shadow-md mt-2"
                disabled={isLoading}
              >
                {isLoading ? (
                  <motion.div
                    className="h-5 w-5 rounded-full border-2 border-white border-t-transparent"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  />
                ) : (
                  <>
                    <UserPlus className="h-4 w-4" />
                    Create Account
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        <p className="mt-5 text-center text-sm text-gray-500 dark:text-gray-400">
          Already have an account?{" "}
          <Link href="/login" className="font-semibold text-dusty-rose-500 hover:text-dusty-rose-600 transition-colors">
            Sign In
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
