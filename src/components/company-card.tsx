import Link from 'next/link';
import type { Investigation } from '@/lib/investigation-types';
import { getSector } from '@/lib/sectors';

export function CompanyCard({ investigation }: { investigation: Investigation }) {
  const sector = getSector(investigation.sectorSlug);
  const href = `/companies/${investigation.sectorSlug}/${investigation.slug}`;

  return (
    <div className="flex flex-col rounded-[1.5rem] border border-black/10 bg-white/90 p-7 shadow-[0_10px_40px_rgba(0,0,0,0.03)]">
      <div className="flex flex-wrap items-center gap-2">
        {sector ? (
          <span className="rounded-full border border-black/10 px-3 py-1 text-sm uppercase tracking-[0.15em] text-black/60">
            {sector.name}
          </span>
        ) : null}
        {investigation.status === 'hold' ? (
          <span className="rounded-full border border-black/30 px-3 py-1 text-sm uppercase tracking-[0.15em] text-black/70">
            Held — internal preview
          </span>
        ) : null}
      </div>
      <h3 className="mt-5 text-lg font-semibold text-ink">{investigation.name}</h3>
      <p className="mt-3 text-sm uppercase tracking-[0.2em] text-black/50">CHI disposition</p>
      <p className="mt-2 text-base text-black/80">
        {investigation.disposition}
        <span className="text-black/50"> · {investigation.dispositionNote}</span>
      </p>
      <p className="mt-5 text-base leading-8 text-black/70">{investigation.summary}</p>
      <div className="mt-auto pt-6">
        <Link
          href={href}
          className="inline-flex rounded-full border border-black/20 px-4 py-2 text-sm font-medium transition hover:border-ink hover:bg-black/5"
        >
          View Research
        </Link>
      </div>
    </div>
  );
}
