import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Header from '@/components/Header';
import { cn } from '@/lib/utils';

const inter = Inter({ subsets: ['latin', 'vietnamese'] });

export const metadata: Metadata = {
  title: 'GitHubDaily Vietnamese Discovery Portal',
  description: 'Khám phá các dự án mã nguồn mở hữu ích từ GitHubDaily, được dịch sang tiếng Việt.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi" className="scroll-smooth">
      <body className={cn("min-h-screen bg-background font-sans antialiased text-slate-900", inter.className)}>
        <div className="relative flex min-h-screen flex-col">
          <Header />
          <main className="flex-1">{children}</main>
        </div>
      </body>
    </html>
  );
}
