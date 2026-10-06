import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CompanyCard } from '@/components/company-card';
import { Navigation } from '@/components/navigation';
import { getVisibleInvestigationsForSector } from '@/lib/companies';
import { getSector, sectors } from '@/lib/sectors';

export const dynamicParams = false;

export function generateStaticParams() {
  return sectors.map((sector) => ({ sector: sector.slug }));
}

type Params = Promise<{ sector: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { sector: slug } = await params;
  const sector = getSector(slug);
  if (!sector) return {};
  return {
    title: `${sector.name} | Customer Hostility Index`,
    description: sector.description,
  };
}

export default async function SectorPage({ params }: { params: Params }) {
  const { sector: slug } = await params;
  const sector = getSector(slug);
  if (!sector) notFound();
  const companies = getVisibleInvestigationsForSector(sector.slug);

  return (
    <main className="min-h-screen bg-paper text-ink">
      <Navigation />
      <section className="mx-auto max-w-5xl px-6 py-20 lg:px-8">
        <nav aria-label="Breadcrumb" className="text-sm text-black/60">
          <Link href="/companies" className="transition hover:text-ink">
            Companies
          </Link>
          <span className="px-2">/</span>
          <span className="text-ink">{sector.name}</span>
        </nav>
        <p className="mt-8 text-sm uppercase tracking-[0.3em] text-black/60">Sector</p>
        <h1 className="mt-4 text-4xl font-semibold sm:text-5xl">{sector.name}</h1>
        <p className="mt-8 max-w-3xl text-lg text-black/70">{sector.description}</p>

        <div className="mt-14 border-t border-black/10 pt-12">
          <p className="text-sm uppercase tracking-[0.3em] text-black/60">Company investigations</p>
          {companies.length > 0 ? (
            <div className="mt-10 grid gap-5 md:grid-cols-2">
              {companies.map((company) => (
                <CompanyCard key={company.slug} investigation={company} />
              ))}
            </div>
          ) : (
            <p className="mt-6 text-base text-black/60">No investigations in this sector have been published yet.</p>
          )}
        </div>
      </section>
    </main>
  );
}
