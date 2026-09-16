import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SignalStack — technical signal, not noise",
  description: "A private, source-backed technical briefing shaped by your work.",
  icons: { icon: "/favicon.svg" }
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
