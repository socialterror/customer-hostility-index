import Link from 'next/link';

export default function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-paper px-6 text-center text-ink">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">404</p>
        <h1 className="mt-4 text-3xl font-semibold">This page is still being drafted.</h1>
        <Link href="/" className="mt-8 inline-flex rounded-full border border-ink bg-ink px-5 py-3 text-sm font-medium text-paper">
          Return home
        </Link>
      </div>
    </main>
  );
}
