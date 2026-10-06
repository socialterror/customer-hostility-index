export type Sector = {
  slug: string;
  name: string;
  description: string;
};

// Sector registry. New sectors are added here; company pages reference a sector by slug.
export const sectors: Sector[] = [
  {
    slug: 'gambling',
    name: 'Gambling',
    description:
      'Companies whose core products involve wagering, betting or gambling-related customer economics.',
  },
];

export function getSector(slug: string): Sector | undefined {
  return sectors.find((sector) => sector.slug === slug);
}
