'use client';

import Link from 'next/link';
import { useState } from 'react';

const navItems = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/about' },
  { label: 'Methodology', href: '/methodology' },
  { label: 'Lexicon', href: '/lexicon' },
  { label: 'Companies', href: '/companies' },
  { label: 'Articles', href: '/articles' },
  { label: 'Contact', href: '/contact' },
];

export function Navigation() {
  const [open, setOpen] = useState(false);

  return (
    <header className="border-b border-black/10">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5 lg:px-8">
        <Link href="/" className="text-sm font-semibold uppercase tracking-[0.3em]">
          CHI
        </Link>

        <button
          type="button"
          className="rounded-full border border-black/20 px-3 py-2 text-sm md:hidden"
          onClick={() => setOpen((value) => !value)}
          aria-label="Toggle navigation"
        >
          Menu
        </button>

        <nav className="hidden gap-6 text-sm text-black/70 md:flex">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="transition hover:text-ink">
              {item.label}
            </Link>
          ))}
        </nav>
      </div>

      {open ? (
        <div className="border-t border-black/10 bg-paper px-6 py-4 md:hidden">
          <nav className="flex flex-col gap-3 text-sm text-black/70">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href} className="transition hover:text-ink" onClick={() => setOpen(false)}>
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      ) : null}
    </header>
  );
}
