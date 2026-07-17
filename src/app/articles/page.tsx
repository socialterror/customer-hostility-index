import { Navigation } from '@/components/navigation';

export default function ArticlesPage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">Articles</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">Essays and analysis on customer experience, power, and accountability.</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">
          This section will gather reporting and commentary that examine how companies behave when customers seek help, challenge decisions, or ask for fairness.
        </p>
      </section>
    </main>
  );
}
