import { Navigation } from '@/components/navigation';

export default function CompaniesPage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">Companies</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">A public record of corporate behavior, examined closely.</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">
          Company research will be organized around documented interactions, recurring patterns, and the broader context in which customers experience service, support, and accountability.
        </p>
      </section>
    </main>
  );
}
