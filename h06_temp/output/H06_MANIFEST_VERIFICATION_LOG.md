# H06 Manifest Verification and Freeze Log

**STATUS: FROZEN — READY FOR BLIND T0 SEMANTIC SCORING**

## Corrected pre-T0 construction

- Historical cutoff: **2020-11-30**
- Historical securities from immutable membership source: **505**
- Issuers after one-CIK collapse: **500**
- Prior H04/H05 issuer CIK exclusions present in historical universe: **65**
- Candidate issuers before SEC filing screen: **435**
- Technical filing-ineligible issuers: **6**
- Final eligible issuers: **429**
- Selected companies: **225**
- Exact verified filings: **1,125**
- F5 window: **2020-08-15 through 2020-11-30**
- Forms: **10-Q / 10-K only**
- Duplicate issuer/accession pairs: **0**
- Outcome research: **CLOSED / NOT USED**
- Semantic scoring: **NOT STARTED**

## Correction rationale

The superseded pre-verification draw was not promoted to the final manifest because its recorded eligible-universe reserve was not reproducible and FRC failed the frozen F5 eligibility rule. The universe was therefore rebuilt before T0 from immutable source blobs, SEC filing eligibility was applied before selection, and the same prespecified random seed and Hamilton sector-allocation method were reapplied. No H06 semantic or outcome information was used.

## Freeze statement

The corrected 225-company / 1,125-filing H06 manifest is frozen. No company or filing may be substituted after this point absent a documented genuine manifest error. The next permitted research operation is blind T0 semantic scoring.
