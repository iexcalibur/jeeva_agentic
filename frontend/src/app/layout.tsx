import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Header from '@/components/Header';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Jeeva Agentic | Persona Switching AI Assistant',
  description: 'An intelligent chatbot that adapts between mentor, investor, technical advisor, and business expert personas',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased bg-slate-950`}>
        <Header />
        {children}
      </body>
    </html>
  );
}
