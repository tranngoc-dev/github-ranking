import React from 'react';
import { FolderGit, Globe } from 'lucide-react';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-14 items-center px-4">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <FolderGit className="h-6 w-6" />
            <span className="hidden font-bold sm:inline-block">
              GitHubDaily VI
            </span>
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center">
            <a
              href="https://tulanh.vercel.app/"
              target="_blank"
              rel="noreferrer"
              className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              <Globe className="h-4 w-4" />
              <span>Tulanh</span>
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}
