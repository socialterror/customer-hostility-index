import Link from 'next/link';
import { Navigation } from '@/components/navigation';
import { RichText } from '@/components/rich-text';
import { DISPOSITION_SCALE, type Investigation, type PatternVerdict } from '@/lib/investigation-types';
import type { Sector } from '@/lib/sectors';

const sectionClass = 'mx-auto max-w-5xl px-6 py-12 lg:px-8';
const cardClass = 'rounded-[1.5rem] border border-black/10 bg-white/90 p-7 shadow-[0_10px_40px_rgba(0,0,0,0.03)]';

function SectionHeading({ eyebrow, title }: { eyebrow: string; title: string }) {
  return (
    <>
      <p className="text-sm uppercase tracking-[0.3em] text-black/60">{eyebrow}</p>
      <h2 className="mt-4 text-2xl font-semibold leading-tight text-ink sm:text-3xl">{title}</h2>
    </>
  );
}

function verdictClass(verdict: PatternVerdict): string {
  switch (verdict) {
    case 'SUPPORTED':
      return 'border-ink bg-ink text-paper';
    case 'WEAKLY SUPPORTED':
      return 'border-ink text-ink';
    default:
      return 'border-black/20 text-black/60';
  }
}

export function InvestigationPage({ investigation, sector }: { investigation: Investigation; sector: Sector }) {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />

      {/* 1. Hero */}
      <section className="mx-auto max-w-5xl px-6 pb-12 pt-16 lg:px-8 lg:pt-20">
        <nav aria-label="Breadcrumb" className="text-sm text-black/60">
          <Link href="/companies" className="transition hover:text-ink">
            Companies
          </Link>
          <span className="px-2">/</span>
          <Link href={`/companies/${sector.slug}`} className="transition hover:text-ink">
            {sector.name}
          </Link>
          <span className="px-2">/</span>
          <span className="text-ink">{investigation.name}</span>
        </nav>
        <div className="mt-8 flex flex-wrap items-center gap-2">
          <span className="rounded-full border border-black/10 px-3 py-1 text-sm uppercase tracking-[0.15em] text-black/60">
            {sector.name}
          </span>
          {investigation.status === 'hold' ? (
            <span className="rounded-full border border-black/30 px-3 py-1 text-sm uppercase tracking-[0.15em] text-black/70">
              Held — internal preview
            </span>
          ) : null}
        </div>
        <h1 className="mt-5 text-4xl font-semibold sm:text-5xl">{investigation.name}</h1>
        <p className="mt-3 text-sm uppercase tracking-[0.2em] text-black/50">{investigation.investigationLabel}</p>
        <p className="mt-8 max-w-3xl text-lg leading-8 text-black/75">{investigation.summary}</p>

        <div className={`mt-10 ${cardClass}`}>
          <p className="text-sm uppercase tracking-[0.3em] text-black/50">CHI evidentiary disposition</p>
          <p className="mt-3 text-2xl font-semibold text-ink">{investigation.disposition}</p>
          <p className="mt-1 text-base text-black/60">{investigation.dispositionNote}</p>
          <ul className="mt-6 flex flex-wrap gap-2" aria-label="Disposition scale">
            {DISPOSITION_SCALE.map((band) => (
              <li
                key={band}
                className={`rounded-full border px-3 py-1 text-sm uppercase tracking-[0.12em] ${
                  band === investigation.disposition ? 'border-ink bg-ink text-paper' : 'border-black/10 text-black/50'
                }`}
              >
                {band}
              </li>
            ))}
          </ul>
          <p className="mt-6 text-sm text-black/50">Date of record: {investigation.dateOfRecord}</p>
        </div>
      </section>

      {/* 2. Why CHI investigated */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Why CHI investigated" title={`Why ${investigation.name}`} />
          <div className="mt-6 max-w-3xl space-y-5 text-lg leading-8 text-black/75">
            {investigation.why.paragraphs.map((paragraph) => (
              <p key={paragraph}>
                <RichText text={paragraph} />
              </p>
            ))}
          </div>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            <div className={cardClass}>
              <p className="text-sm uppercase tracking-[0.2em] text-black/50">Thesis tested</p>
              <p className="mt-3 text-base leading-8 text-black/80">{investigation.why.thesis}</p>
            </div>
            <div className={cardClass}>
              <p className="text-sm uppercase tracking-[0.2em] text-black/50">Null hypothesis</p>
              <p className="mt-3 text-base leading-8 text-black/80">{investigation.why.nullHypothesis}</p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Executive finding */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Executive finding" title="What the evidence shows" />
          <div className="mt-6 max-w-3xl space-y-5 text-lg leading-8 text-black/75">
            {investigation.executive.map((paragraph, index) => (
              <p key={paragraph} className={index === 0 ? 'font-semibold text-ink' : undefined}>
                <RichText text={paragraph} />
              </p>
            ))}
          </div>
        </div>
      </section>

      {/* 4. Key findings */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Key findings" title="The findings that shaped the result" />
          <div className="mt-8 space-y-5">
            {investigation.findings.map((finding, index) => (
              <article key={finding.title} className={cardClass}>
                <p className="text-sm text-black/50">Finding {index + 1}</p>
                <h3 className="mt-2 text-xl font-semibold leading-snug text-ink">{finding.title}</h3>
                <dl className="mt-5 space-y-4">
                  {[
                    ['Fact', finding.fact],
                    ['Evidence', finding.evidence],
                    ['Implication', finding.implication],
                  ].map(([label, body]) => (
                    <div key={label}>
                      <dt className="text-sm uppercase tracking-[0.2em] text-black/50">{label}</dt>
                      <dd className="mt-1 text-base leading-8 text-black/80">
                        <RichText text={body} />
                      </dd>
                    </div>
                  ))}
                </dl>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* 5. Strongest counterevidence */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Strongest counterevidence" title="What argues against the hostile thesis" />
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            {investigation.counterevidence.map((item) => (
              <div key={item.title} className={cardClass}>
                <h3 className="text-lg font-semibold text-ink">{item.title}</h3>
                <p className="mt-3 text-base leading-8 text-black/75">
                  <RichText text={item.body} />
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 6. SP001–SP004 */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Semantic patterns" title="SP001–SP004" />
          <p className="mt-4 max-w-3xl text-base leading-8 text-black/70">
            Each pattern from the CHI Semantic Pattern Taxonomy is adjudicated independently. A pattern marked not supported
            or insufficient evidence is not present on the record CHI examined.
          </p>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            {investigation.patterns.map((pattern) => (
              <div key={pattern.id} className={cardClass}>
                <p className="text-sm uppercase tracking-[0.2em] text-black/50">{pattern.id}</p>
                <h3 className="mt-2 text-lg font-semibold text-ink">{pattern.name}</h3>
                <div className="mt-4 flex flex-wrap items-center gap-3">
                  <span className={`rounded-full border px-3 py-1 text-sm uppercase tracking-[0.12em] ${verdictClass(pattern.verdict)}`}>
                    {pattern.verdict}
                  </span>
                  {pattern.confidence ? (
                    <span className="text-sm text-black/60">Confidence: {pattern.confidence}</span>
                  ) : null}
                </div>
                <p className="mt-4 text-base leading-8 text-black/75">
                  <RichText text={pattern.explanation} />
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 7. Customer relationship over time */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Customer relationship over time" title="How the relationship has changed" />
          <ol className="mt-8 space-y-8 border-l border-black/10 pl-6">
            {investigation.timeline.map((period) => (
              <li key={period.period}>
                <h3 className="text-lg font-semibold text-ink">{period.period}</h3>
                <p className="mt-2 max-w-3xl text-base leading-8 text-black/75">
                  <RichText text={period.body} />
                </p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* 8. What the evidence means */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="What the evidence means" title="For the customer relationship" />
          <dl className="mt-8 space-y-6">
            {investigation.meaning.map((item) => (
              <div key={item.label} className="grid gap-2 md:grid-cols-[12rem_1fr] md:gap-8">
                <dt className="text-sm uppercase tracking-[0.2em] text-black/50 md:pt-1">{item.label}</dt>
                <dd className="text-base leading-8 text-black/80">
                  <RichText text={item.body} />
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* 9. Unresolved questions / limitations */}
      <section className={sectionClass}>
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Unresolved questions" title="What remains open" />
          <ul className="mt-6 max-w-3xl list-disc space-y-3 pl-5 text-base leading-8 text-black/75">
            {investigation.unresolved.map((item) => (
              <li key={item}>
                <RichText text={item} />
              </li>
            ))}
          </ul>
          <p className="mt-6 max-w-3xl text-base leading-8 text-black/60">
            <RichText text={investigation.limitationsNote} />
          </p>
        </div>
      </section>

      {/* 10. Sources and methodology */}
      <section className="mx-auto max-w-5xl px-6 pb-24 pt-12 lg:px-8">
        <div className="border-t border-black/10 pt-12">
          <SectionHeading eyebrow="Sources and methodology" title="How CHI reached this result" />
          <div className="mt-6 max-w-3xl space-y-4 text-base leading-8 text-black/75">
            {investigation.methodology.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
          <h3 className="mt-10 text-lg font-semibold text-ink">Selected sources</h3>
          <ul className="mt-4 divide-y divide-black/10 border-y border-black/10">
            {investigation.sources.map((source) => (
              <li key={source.title} className="flex flex-col gap-1 py-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-6">
                <div>
                  {source.url ? (
                    <a href={source.url} className="text-base text-ink underline decoration-black/20 underline-offset-4 transition hover:decoration-ink" rel="noopener noreferrer" target="_blank">
                      {source.title}
                    </a>
                  ) : (
                    <span className="text-base text-ink">{source.title}</span>
                  )}
                  <p className="text-sm text-black/60">
                    {source.publisher} · {source.date}
                  </p>
                </div>
                <span className="shrink-0 text-sm uppercase tracking-[0.15em] text-black/50">{source.kind}</span>
              </li>
            ))}
          </ul>
          <Link href={`/companies/${sector.slug}`} className="mt-10 inline-flex rounded-full border border-black/20 px-5 py-3 text-sm font-medium transition hover:border-ink hover:bg-black/5">
            Back to {sector.name}
          </Link>
        </div>
      </section>
    </main>
  );
}
