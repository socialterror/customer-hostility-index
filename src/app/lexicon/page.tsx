import { Navigation } from '@/components/navigation';

export default function LexiconPage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">Lexicon</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">A careful vocabulary for describing customer friction.</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">
          Words matter. This section defines terms used to distinguish between inconvenience, harm, coercion, and disrespect, with an emphasis on precision rather than exaggeration.
        </p>
      </section>
    </main>
  );
}
