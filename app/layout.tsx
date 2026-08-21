import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SignalStack",
  description:
    "A tech-only personalized intelligence website that surfaces the updates that actually matter."
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
