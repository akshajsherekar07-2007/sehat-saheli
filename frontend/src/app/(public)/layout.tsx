"use client";

/**
 * Public layout — wraps pages that are accessible without authentication.
 * Provides TopBar and BottomNav but does NOT require login.
 */

import { type ReactNode } from "react";
import { TopBar, BottomNav, OfflineBanner, ToastContainer } from "@/components/layout";

export default function PublicLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <OfflineBanner />
      <TopBar />
      <main className="flex-1 pb-nav">{children}</main>
      <BottomNav />
      <ToastContainer />
    </div>
  );
}
