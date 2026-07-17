import { Navigation } from '@/components/navigation';

export default function MethodologyPage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">Methodology</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">A transparent system for interpreting customer experience with discipline.</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">
          The methodology is designed to separate evidence from rhetoric. It evaluates how companies communicate, respond, and behave across repeatable situations, while making clear which claims are documented and which remain unresolved.
        </p>
      </section>
    </main>
  );
}
