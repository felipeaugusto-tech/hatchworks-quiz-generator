import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "HatchWorks Quiz Generator",
  description: "Upload a recording, transcribe it, and generate a quiz.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}