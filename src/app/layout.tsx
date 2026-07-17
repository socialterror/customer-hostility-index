import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Customer Hostility Index',
  description: 'A modern index for measuring how companies treat customers.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="bg-paper">
      <body>{children}</body>
    </html>
  );
}
