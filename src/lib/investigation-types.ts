export type PublicationStatus = 'published' | 'hold';

export type Disposition =
  | 'NOT SUPPORTED'
  | 'INCONCLUSIVE'
  | 'WEAKLY SUPPORTS'
  | 'PARTIALLY SUPPORTS'
  | 'SUPPORTS'
  | 'STRONGLY SUPPORTS';

export const DISPOSITION_SCALE: Disposition[] = [
  'NOT SUPPORTED',
  'INCONCLUSIVE',
  'WEAKLY SUPPORTS',
  'PARTIALLY SUPPORTS',
  'SUPPORTS',
  'STRONGLY SUPPORTS',
];

export type PatternVerdict = 'SUPPORTED' | 'WEAKLY SUPPORTED' | 'NOT SUPPORTED' | 'INSUFFICIENT EVIDENCE';

export type PatternResult = {
  id: 'SP001' | 'SP002' | 'SP003' | 'SP004';
  name: string;
  verdict: PatternVerdict;
  confidence?: string;
  explanation: string;
};

export type KeyFinding = {
  title: string;
  fact: string;
  evidence: string;
  implication: string;
};

export type Counterpoint = {
  title: string;
  body: string;
};

export type TimelinePeriod = {
  period: string;
  body: string;
};

export type MeaningItem = {
  label: string;
  body: string;
};

export type SourceItem = {
  title: string;
  publisher: string;
  date: string;
  url?: string;
  kind: 'Primary document' | 'Reported';
};

export type Investigation = {
  slug: string;
  name: string;
  sectorSlug: string;
  status: PublicationStatus;
  investigationLabel: string;
  dateOfRecord: string;
  disposition: Disposition;
  dispositionNote: string;
  summary: string;
  why: {
    paragraphs: string[];
    thesis: string;
    nullHypothesis: string;
  };
  executive: string[];
  findings: KeyFinding[];
  counterevidence: Counterpoint[];
  patterns: PatternResult[];
  timeline: TimelinePeriod[];
  meaning: MeaningItem[];
  unresolved: string[];
  limitationsNote: string;
  sources: SourceItem[];
  methodology: string[];
};
