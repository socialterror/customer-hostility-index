import { Navigation } from '@/components/navigation';

export default function ContactPage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <p className="text-sm uppercase tracking-[0.3em] text-black/60">Contact</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">Contact the editorial team about research, collaboration, or public inquiry.</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">
          The project is intended for rigorous public study. Contact is available for researchers, journalists, and readers who want to discuss methods, evidence, or findings.
        </p>
      </section>
    </main>
  );
}
