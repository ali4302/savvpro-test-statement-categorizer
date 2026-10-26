import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Statement Categorizer',
  description: 'Categorize bank and credit-card statements for tax time.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
