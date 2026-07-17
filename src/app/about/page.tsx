import { Navigation } from '@/components/navigation';

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">About</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">An investigative framework for understanding how companies treat people under pressure.</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">
          CHI is built around the idea that customer experience should be examined with the same discipline and rigor used in journalism, research, and public accountability. The work is grounded in evidence, context, and clear standards rather than branding language or anecdotal claims.
        </p>
      </section>
    </main>
  );
}
