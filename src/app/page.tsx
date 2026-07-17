import Link from 'next/link';
import { Navigation } from '@/components/navigation';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />

      <section className="mx-auto flex min-h-[calc(100vh-80px)] w-full max-w-7xl flex-col justify-center px-6 py-24 lg:px-8 lg:py-28">
        <div className="grid gap-16 lg:grid-cols-[1.15fr_0.85fr] lg:gap-20">
          <div className="mx-auto flex max-w-3xl flex-col justify-center">
          <p className="mb-6 text-sm font-medium uppercase tracking-[0.35em] text-black/60">
            Customer Hostility Index
          </p>
          <h1 className="text-[2.2rem] font-semibold leading-[0.95] sm:text-[2.7rem] lg:text-[4.4rem]">
            Transforming subjective customer experiences into objective, evidence-based analysis.
          </h1>
          <h2 className="mt-8 text-xl font-semibold leading-tight text-black/85 sm:text-2xl">
            Companies have spent decades measuring customers.
          </h2>
          <p className="mt-3 text-lg leading-8 text-black/70">
            It&apos;s time customers started measuring companies.
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/methodology"
              className="rounded-full border border-ink bg-ink px-5 py-3 text-sm font-medium text-paper transition hover:bg-black"
            >
              Explore the Methodology
            </Link>
            <Link
              href="/companies"
              className="rounded-full border border-black/20 px-5 py-3 text-sm font-medium transition hover:border-ink hover:bg-black/5"
            >
              Browse Company Research
            </Link>
          </div>
        </div>

          <div className="self-start rounded-[2rem] border border-black/10 bg-white/90 p-8 shadow-[0_20px_80px_rgba(0,0,0,0.05)] backdrop-blur-sm">
            <p className="text-sm uppercase tracking-[0.3em] text-black/50">What CHI is</p>
            <div className="mt-7 space-y-6">
              <div className="border-b border-black/10 pb-5">
                <p className="text-sm text-black/50">Scope</p>
                <p className="mt-2 text-base leading-8 text-black/80">
                  CHI is a framework for examining how companies communicate, respond, and behave when customers encounter friction.
                </p>
              </div>
              <div className="border-b border-black/10 pb-5">
                <p className="text-sm text-black/50">Approach</p>
                <p className="mt-2 text-base leading-8 text-black/80">
                  It brings together public evidence, documented customer experience, and rigorous analysis rather than opinion alone.
                </p>
              </div>
              <div>
                <p className="text-sm text-black/50">Purpose</p>
                <p className="mt-2 text-base leading-8 text-black/80">
                  The goal is not to sensationalize, but to create a clearer and more accountable record of corporate behavior.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-24 lg:px-8 lg:py-28">
        <div className="border-t border-black/10 pt-12">
          <p className="text-sm uppercase tracking-[0.3em] text-black/60">What CHI Measures</p>
          <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {[
              ['Revenue Extraction', 'How companies monetize customer dependence through pricing, fees, and coercive design.'],
              ['Behavioral Manipulation', 'How interfaces, timing, and language steer users toward choices that benefit the company.'],
              ['Customer Restriction', 'How access, support, and flexibility are deliberately narrowed or made difficult.'],
              ['Information & Privacy', 'How companies collect, obscure, and control information that affects user agency.'],
            ].map(([title, description]) => (
              <div key={title} className="rounded-[1.5rem] border border-black/10 bg-white/90 p-7 shadow-[0_10px_40px_rgba(0,0,0,0.03)]">
                <h3 className="text-lg font-semibold text-ink">{title}</h3>
                <p className="mt-3 text-sm leading-8 text-black/70">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-24 lg:px-8 lg:py-28">
        <div className="border-t border-black/10 pt-12">
          <p className="text-sm uppercase tracking-[0.3em] text-black/60">Featured Company Research</p>
          <div className="mt-10 grid gap-5 lg:grid-cols-3">
            {[
              {
                company: 'Netflix',
                primaryPattern: 'Price Creep',
                supportingPatterns: 'Advertising Creep · Access Downgrading',
              },
              {
                company: 'Prime Video',
                primaryPattern: 'Feature Fragmentation',
                supportingPatterns: 'Platform Lock-In · Information Friction',
              },
              {
                company: 'Disney+',
                primaryPattern: 'Artificial Scarcity',
                supportingPatterns: 'Price Creep · Platform Lock-In',
              },
            ].map((item) => (
              <div key={item.company} className="rounded-[1.5rem] border border-black/10 bg-white/90 p-7 shadow-[0_10px_40px_rgba(0,0,0,0.03)]">
                <h3 className="text-lg font-semibold text-ink">{item.company}</h3>
                <p className="mt-3 text-sm uppercase tracking-[0.2em] text-black/50">Primary pattern</p>
                <p className="mt-2 text-base text-black/80">{item.primaryPattern}</p>
                <p className="mt-5 text-sm uppercase tracking-[0.2em] text-black/50">Supporting patterns</p>
                <p className="mt-2 text-base text-black/80">{item.supportingPatterns}</p>
                <Link href="/companies" className="mt-6 inline-flex rounded-full border border-black/20 px-4 py-2 text-sm font-medium transition hover:border-ink hover:bg-black/5">
                  View Research
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-24 lg:px-8 lg:py-28">
        <div className="border-t border-black/10 pt-12">
          <p className="text-sm uppercase tracking-[0.3em] text-black/60">Learn the Language</p>
          <div className="mt-8 flex flex-col gap-8 rounded-[1.5rem] border border-black/10 bg-white/90 p-8 shadow-[0_10px_40px_rgba(0,0,0,0.03)] lg:flex-row lg:items-start lg:justify-between lg:p-10">
            <div className="max-w-2xl">
              <p className="text-lg leading-8 text-black/80">
                The CHI Lexicon gives shape to recurring patterns of customer friction, coercion, and restriction. These terms are meant to clarify what is happening in practice rather than simply name it.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {['Price Creep', 'Advertising Creep', 'Feature Fragmentation', 'Access Downgrading', 'Artificial Scarcity', 'Platform Lock-In'].map((term) => (
                <span key={term} className="rounded-full border border-black/10 px-3 py-2 text-sm text-black/70">
                  {term}
                </span>
              ))}
            </div>
          </div>
          <Link href="/lexicon" className="mt-8 inline-flex rounded-full border border-ink bg-ink px-5 py-3 text-sm font-medium text-paper transition hover:bg-black">
            Explore the Lexicon
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-24 lg:px-8 lg:py-28">
        <div className="border-t border-black/10 pt-16 text-center">
          <h2 className="mx-auto max-w-3xl text-3xl font-semibold leading-tight text-ink sm:text-4xl">
            Companies have measured customers for decades.
          </h2>
          <p className="mt-4 text-lg text-black/70">
            It&apos;s time customers had a framework for measuring companies.
          </p>
          <Link href="/methodology" className="mt-8 inline-flex rounded-full border border-ink bg-ink px-5 py-3 text-sm font-medium text-paper transition hover:bg-black">
            Explore the Methodology
          </Link>
        </div>
      </section>
    </main>
  );
}
