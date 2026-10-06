import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { InvestigationPage } from '@/components/investigation-page';
import { getVisibleInvestigation, getVisibleInvestigations } from '@/lib/companies';
import { getSector } from '@/lib/sectors';

// Only visible investigations are generated; held investigations return 404 unless CHI_SHOW_HELD=true.
export const dynamicParams = false;

export function generateStaticParams() {
  return getVisibleInvestigations().map((investigation) => ({
    sector: investigation.sectorSlug,
    company: investigation.slug,
  }));
}

type Params = Promise<{ sector: string; company: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { sector, company } = await params;
  const investigation = getVisibleInvestigation(sector, company);
  if (!investigation) return {};
  return {
    title: `${investigation.name} | Customer Hostility Index`,
    description: investigation.summary,
    robots: investigation.status === 'hold' ? { index: false, follow: false } : undefined,
  };
}

export default async function CompanyInvestigationPage({ params }: { params: Params }) {
  const { sector: sectorSlug, company } = await params;
  const sector = getSector(sectorSlug);
  const investigation = getVisibleInvestigation(sectorSlug, company);
  if (!sector || !investigation) notFound();
  return <InvestigationPage investigation={investigation} sector={sector} />;
}
