import { draftkings } from '@/content/investigations/draftkings';
import { fanduel } from '@/content/investigations/fanduel';
import type { Investigation } from '@/lib/investigation-types';

// Company registry. Add new investigations here; each references its sector by slug.
const investigations: Investigation[] = [draftkings, fanduel];

// Publication control. Investigations with status 'hold' are excluded from every listing,
// route and static build unless CHI_SHOW_HELD=true is set (internal preview builds only).
export const showHeld = process.env.CHI_SHOW_HELD === 'true';

export function isVisible(investigation: Investigation): boolean {
  return investigation.status === 'published' || showHeld;
}

export function getVisibleInvestigations(): Investigation[] {
  return investigations.filter(isVisible);
}

export function getVisibleInvestigationsForSector(sectorSlug: string): Investigation[] {
  return getVisibleInvestigations()
    .filter((investigation) => investigation.sectorSlug === sectorSlug)
    .sort((a, b) => a.name.localeCompare(b.name));
}

export function getVisibleInvestigation(sectorSlug: string, slug: string): Investigation | undefined {
  return getVisibleInvestigations().find(
    (investigation) => investigation.sectorSlug === sectorSlug && investigation.slug === slug,
  );
}
