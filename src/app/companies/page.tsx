import Link from 'next/link';
import { CompanyCard } from '@/components/company-card';
import { Navigation } from '@/components/navigation';
import { getVisibleInvestigationsForSector } from '@/lib/companies';
import { sectors } from '@/lib/sectors';

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

        {sectors.map((sector) => {
          const companies = getVisibleInvestigationsForSector(sector.slug);
          return (
            <div key={sector.slug} className="mt-16 border-t border-black/10 pt-12">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                <div>
                  <p className="text-sm uppercase tracking-[0.3em] text-black/60">Sector</p>
                  <h2 className="mt-3 text-2xl font-semibold text-ink sm:text-3xl">{sector.name}</h2>
                  <p className="mt-3 max-w-2xl text-base leading-8 text-black/70">{sector.description}</p>
                </div>
                <Link
                  href={`/companies/${sector.slug}`}
                  className="inline-flex shrink-0 self-start rounded-full border border-black/20 px-4 py-2 text-sm font-medium transition hover:border-ink hover:bg-black/5 sm:self-auto"
                >
                  View {sector.name}
                </Link>
              </div>
              {companies.length > 0 ? (
                <div className="mt-8 grid gap-5 md:grid-cols-2">
                  {companies.map((company) => (
                    <CompanyCard key={company.slug} investigation={company} />
                  ))}
                </div>
              ) : null}
            </div>
          );
        })}
      </section>
    </main>
  );
}
