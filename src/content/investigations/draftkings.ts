import type { Investigation } from '@/lib/investigation-types';

// Source of truth: chi-research/draftkings/final-deliverables (master dossier, SP001–SP004,
// timeline, source ledger, verification memo), date of record 6 October 2026.
// Publication status: HOLD — SOURCE VERIFICATION. The page is complete but must not be released
// until the controlling sources listed in the verification memo §10.5 have been read.
export const draftkings: Investigation = {
  slug: 'draftkings',
  name: 'DraftKings',
  sectorSlug: 'gambling',
  status: 'hold',
  investigationLabel: 'U.S. online sportsbook · customer-economics investigation',
  dateOfRecord: '6 October 2026',
  disposition: 'PARTIALLY SUPPORTS',
  dispositionNote: 'Lower edge of the band',
  summary:
    'DraftKings runs a competitive, well-rated sportsbook. In its fine print, pricing design and treatment of particular groups of customers — winning bettors, small-stake and base-tier customers — its pursuit of yield is repeatedly visible, sometimes to the point of regulatory correction. It is not hostile across the relationship.',
  why: {
    paragraphs: [
      'DraftKings is one of the two operators that together hold most of the U.S. online sports-betting market, with about four million monthly paying customers in 27 states and the District of Columbia. CHI did not select it because of any prior finding against it.',
      'The public record contained dated, company-sourced statements and regulator actions bearing directly on CHI’s questions: who pays, what they pay, what access they receive, what they are steered toward and what recourse they have. Management has told investors it aims to raise structural hold and optimise promotional spending. DraftKings was the first U.S. operator to announce a tax surcharge on customers’ winnings. Its chief executive has spoken publicly about limiting profit-seeking bettors.',
    ],
    thesis:
      'DraftKings’ U.S. sportsbook shows recurring, evidence-based patterns of customer extraction, asymmetry, access friction, winner limitation, withdrawal friction, promotional manipulation, value deterioration, recourse weakness, or product and enforcement design that shifts risk or cost onto customers.',
    nullHypothesis:
      'DraftKings offers a reasonably competitive product whose pricing, promotions, risk controls, account restrictions, responsible-gambling systems and customer-service procedures are proportionate to the value it delivers and to the regulatory obligations of a large sportsbook.',
  },
  executive: [
    'The evidence partially supports the hostile thesis, at the lower edge of that band.',
    'What drives the result is a set of mechanisms established on DraftKings’ own documents and on regulator records: discretionary limits and voiding rights written into its house rules; promotions whose headline value exceeds what a customer can realise; a tax pass-through fee whose exemptions leave small bets and lower loyalty tiers paying; a request to void most of a customer’s large win caused by DraftKings’ own error, refused by two regulators; and repeated small penalties for failing self-excluded customers.',
    'What limits it is equally clear. Pricing is at the market, payouts are fast, responsible-gambling tools go beyond the legal minimum, independent satisfaction scores are high, penalties are financially immaterial, and no regulator or court has found that DraftKings deceived anyone. The most serious contemporary claims — about VIP hosts and targeted promotions — remain allegations.',
  ],
  findings: [
    {
      title: 'Broad voiding rights, and a regulator-refused attempt to void most of a customer win caused by DraftKings’ own error',
      fact:
        'DraftKings’ Massachusetts house rules allow bets to be voided after settlement and list customer conduct such as “influence” and “syndicate” betting among void grounds. In October 2025 a trader misclassification let a customer place 27 parlays ($12,950 staked) carrying $934,147.83 of liability.',
      evidence:
        'DraftKings asked the Massachusetts Gaming Commission to void only the correlated “lesser” legs, which would have cut the payout to $95,742.53. Commission staff found no direct evidence that the customer knowingly exploited the error, and the Commission refused the request 5–0 on 18 December 2025. New Jersey also refused; Pennsylvania had allowed the partial void. The Massachusetts rule text, staff memo and minutes were read in full.',
      implication:
        'Had the request been granted, most of the cost of the company’s own configuration error would have moved to the customer. Every void in Massachusetts needs regulator approval, and that state requirement is what protected the customer here.',
    },
    {
      title: 'Discretionary limits on winning bettors, linked by management to margin',
      fact:
        'The house rules in force since 26 August 2025 let DraftKings lower any customer’s maximum payout “in its sole and absolute discretion, with or without notice, for any reason or no reason”. Earlier versions limited stakes “on a per user or aggregate basis” but let customers request a higher limit, a route the current version no longer contains.',
      evidence:
        'The chief executive has been reported as describing profit-seeking bettors as “not the players we want” (2021) and limiting sharp action as a route to a better win rate (2022), and in 2025 as the condition for offering a wide range of bets. These remarks come from conference coverage; the transcripts were not read. Journalism and regulator testimony document individual no-notice cases in 2022–2024.',
      implication:
        'Limiting is ordinary risk management at every sportsbook and touches a small group — DraftKings says fewer than 1% of players. What is distinctive is the explicit link to margin and the removal of the request route. Massachusetts has required reasoned notice by state rule since 1 June 2026.',
    },
    {
      title: 'Promotions whose headline exceeds realisable value, and enforcement over sportsbook marketing',
      fact:
        'DraftKings’ long-running “20% deposit match up to $1,000” required 25 times the bonus in wagering, at the less generous end of the market range. For a bettor with no edge who wagers to unlock it, CHI calculates a negative expected value under every assumption.',
      evidence:
        'Ohio approved a $500,000 settlement in February 2023, covering about 2,500 mailers sent to people under 21 and advertising that used “free” and “risk-free” wording without required problem-gambling messaging. Maryland penalised the same mailing. A Massachusetts court let a deposit-match claim proceed past summary judgment in February 2026 (*Scanlon*); that is not a finding of deception. A New York federal court dismissed similar “No Sweat” and deposit-bonus claims in full in December 2025 (*De Leon*), holding that a reasonable consumer “would have read the terms”.',
      implication:
        'The record is one of disclosure and marketing enforcement, not adjudicated deception. Settlements are not admissions. A separate Connecticut refund of $3.01 million concerned casino offers, not the sportsbook.',
    },
    {
      title: 'Explicit tax pass-through, with a design that falls on smaller bets',
      fact:
        'In August 2024 DraftKings announced a surcharge on customers’ net winnings in four high-tax states, saying it would be “fairly nominal to the customer” while creating “additional upside potential” for adjusted EBITDA, then withdrew it twelve days later. In June 2025 it announced a per-bet fee in Illinois “in response to” the state’s per-wager tax, effective 1 September 2025.',
      evidence:
        'As reported, the fee was implemented at 25¢ rising to 50¢, itemised as a pass-through, and not charged on parlays of $10 or more, straight bets of $50 or more, bonus-bet stakes or members of the Silver loyalty tier and above. No waiver was reported. The company’s fee page and filings could not be read for this investigation.',
      implication:
        'This is a clear case of an external cost moved explicitly onto customers. Its effect is that small-stake and lower-tier customers pay while larger bets and higher tiers do not. Whether that was the purpose is disputed: it may protect yield, or reflect what the tax absorbs within margin.',
    },
    {
      title: 'Reduced generosity to existing customers as a stated margin lever',
      fact:
        'In 2024 and 2025 DraftKings reported improving promotional reinvestment as a share of revenue, including, as reported, “reduced promotions for lower-value customer segments”. It guided to a “meaningful decline in promotional intensity in 2025” and later attributed part of its margin gain to it.',
      evidence:
        'In 2026 it removed loyalty earning for its base tier (January) and introduced a twelve-month expiry for its reward currency (August), where it had previously said its loyalty points did not expire. The welcome offer fell from $200 (2023) to a $100 low in spring 2026 and is now paid out in instalments over two weeks.',
      implication:
        'These are deliberate reductions in value for existing customers, disclosed as yield measures. Their scale is modest: loyalty value is about 0.1–0.25% of the amount wagered, and new-customer promotion rose again in 2026.',
    },
    {
      title: 'Repeated small failures in protecting self-excluded customers, and two fund-handling penalties',
      fact:
        'New Jersey penalised DraftKings in 2019, 2021 and 2023 for contacting self-excluded people or failing to stop them from betting. Michigan fined it $5,000 in 2025 because 15 customers exceeded limits they had set themselves.',
      evidence:
        'In Massachusetts, a contested 2025 decision imposed $450,000 for accepting credit-card-funded wagers despite a statutory ban and ordered $83,667.92 refunded to 218 customers, rejecting DraftKings’ “misunderstanding” defence. Michigan, as reported, fined DraftKings $25,000 for holding a $19,028.96 withdrawal for about four months without alleging fraud; that order was not read.',
      implication:
        'Each amount is small and most matters were self-reported, but the self-exclusion category recurs in one jurisdiction across five years. Protections that exist on paper have failed in practice more than once.',
    },
  ],
  counterevidence: [
    {
      title: 'Customers rate it highly',
      body: 'DraftKings placed first in the American Customer Satisfaction Index’s inaugural online-sportsbook ranking in 2025 (78/100, from about 25,000 interviews) and tied for first in 2026, although its score fell that year as the industry cut bonuses.',
    },
    {
      title: 'Prices are at the market and payouts are fast',
      body: 'Its mainline odds are at the market, and an academic test found no detectable price shading. It runs reduced-margin NFL promotions and does not generally cap boosted-odds stakes. CBS Sports’ 2026 testing called it the fastest-paying sportsbook it reviewed, with some withdrawal methods completing within the hour.',
    },
    {
      title: 'Responsible-gambling tools beyond the legal minimum',
      body: 'DraftKings offers cross-product limits on deposits, wagers, losses and time that can be lowered at any time and raised only after a waiting period. It holds an industry safer-gambling award (2024), co-founded the Responsible Online Gaming Association and has funded state problem-gambling councils. Its Massachusetts filings show limit-tool use rising, to about 5.6% of players in 2025.',
    },
    {
      title: 'Penalties are immaterial to the business, and most were self-reported',
      body: 'Its 2024–2025 penalties total about $1.4 million, roughly 0.02% of one year’s revenue (about 0.075% including ordered refunds). Most arose from self-reported process errors, and customers were refunded where regulators ordered it.',
    },
    {
      title: 'Courts have largely sided with DraftKings',
      body: 'No regulator or court has found that DraftKings deceived customers. The New York federal court in *De Leon* dismissed the promotional and VIP-host claims in full and found no duty of care owed to addicted gamblers. Courts upheld contested bet cancellations in 2026, and two VIP-host suits settled without admission.',
    },
    {
      title: 'The surcharge never charged anyone, and the Illinois fee is tied to the tax',
      body: 'The 2024 winnings surcharge was withdrawn before it took effect; DraftKings attributed this to customer feedback. The Illinois fee mirrors a per-bet tax unique to that state, is matched by its main rival and carries a stated commitment to remove it if the tax is repealed.',
    },
    {
      title: 'Limiting touches very few customers, on grounds regulators accept',
      body: 'DraftKings says it limits fewer than 1% of players; across all Massachusetts operators the figure was 0.64% of accounts. No regulator has found the practice unlawful, and no limited customer was found refused an existing balance.',
    },
    {
      title: 'Free and lower-variance features',
      body: 'Free-to-play pools carry cash prizes, and its streaming channel is free without an account. Progressive Parlays pay reduced amounts when not every leg wins, lowering variance for the customer. After a 2025 consumer report, DraftKings added an opt-out for marketing notifications.',
    },
  ],
  patterns: [
    {
      id: 'SP001',
      name: 'Unmonetized Access / Entitlement Monetization',
      verdict: 'NOT SUPPORTED',
      confidence: 'Medium',
      explanation:
        'No previously free feature or entitlement was found moved behind payment. The free streaming channel and free-to-play pools remain free, and the $20-a-month Sportsbook+ tier in New York is an optional premium product rather than a paywall placed over something customers already had.',
    },
    {
      id: 'SP002',
      name: 'Existing-Customer Yield Optimization',
      verdict: 'SUPPORTED',
      confidence: 'Medium',
      explanation:
        'DraftKings reduced and re-targeted promotional reinvestment to its existing base in 2024–2025 and reported the margin effect, including reduced promotions for lower-value segments. It continued in 2026 with the removal of base-tier loyalty earning and a twelve-month expiry on its reward currency. Confidence is Medium because the investor transcripts behind the anchor statement were not read verbatim.',
    },
    {
      id: 'SP003',
      name: 'Legacy Product Deprioritization / Portfolio Concentration',
      verdict: 'NOT SUPPORTED',
      confidence: 'Medium',
      explanation:
        'No product was retired with customers forced to migrate. The 2026 plan to consolidate apps had been announced but not carried out on the evidence available.',
    },
    {
      id: 'SP004',
      name: 'Cost Pressure → Customer Cost Transfer',
      verdict: 'SUPPORTED',
      confidence: 'Medium-High',
      explanation:
        'The Illinois per-bet fee explicitly passes a state per-wager tax to customers and is to be removed if the tax is repealed. The 2024 winnings surcharge was a second, announced-then-withdrawn instance of the same mechanism and is not counted as implemented.',
    },
  ],
  timeline: [
    {
      period: '2018–2022: launch and early promotions',
      body: 'DraftKings launched online sportsbooks state by state from 2018, with welcome offers built around deposit matches and bonus bets. In 2019 New Jersey penalised it twice, once for marketing to self-excluded customers and once for a software defect that let cooling-off customers bet. Its loyalty programme launched in late 2020. In December 2022 an Ohio mailing reached about 2,500 people under 21.',
    },
    {
      period: '2023–2024: enforcement, limiting scrutiny and a withdrawn surcharge',
      body: 'Ohio’s $500,000 settlement (February 2023) and a Maryland penalty addressed that mailing and “risk-free” advertising. Credit-card-funded wagers accepted in Massachusetts in 2023–24 later produced a contested $450,000 decision. Limiting drew public attention after documented cases and a 2024 regulator roundtable. In August 2024 DraftKings announced, then withdrew, a surcharge on winnings in four high-tax states.',
    },
    {
      period: '2025: promotional discipline and the Illinois fee',
      body: 'DraftKings told investors promotional intensity would fall meaningfully in 2025. In June it announced the Illinois per-bet fee, live from 1 September with reported exemptions for larger bets and higher loyalty tiers. Michigan fined it over a withheld withdrawal and over customers exceeding self-set limits. On 26 August its Massachusetts house rules were rewritten, adding the “with or without notice” payout-limit wording and a $1.65 million cap. In October a trader error led to the Lukes parlays, and in December two regulators refused DraftKings’ request to void most of that win. The same month a New York federal court dismissed the *De Leon* promotional and VIP-host claims in full.',
    },
    {
      period: '2026: value trimmed for existing customers, generosity back for new ones',
      body: 'Base-tier loyalty earning was removed in January, and a twelve-month expiry on the renamed reward currency followed in August. The welcome offer reached a $100 low in spring, while overall promotion rose again for new customers. Massachusetts began requiring reasoned notice of betting limits on 1 June. In September, investigative reporting raised questions about how promotions are targeted; that matter is press-reported and no regulator finding exists.',
    },
  ],
  meaning: [
    {
      label: 'Customer value',
      body: 'The core product is good value: market-level prices, fast payouts, broad markets and above-minimum safety tools. Most customers who place ordinary bets and withdraw their winnings meet none of the mechanisms described here.',
    },
    {
      label: 'Extraction',
      body: 'Where extraction appears, it is deliberate and disclosed rather than hidden: less promotional value for existing and lower-value customers, a tax passed through with exemptions that spare larger bets, and loyalty value trimmed in 2026. It is modest in size and partly reversed for new customers.',
    },
    {
      label: 'Asymmetry',
      body: 'The clearest asymmetry is in the house rules. DraftKings can limit any customer, refuse any bet, re-settle bets and seek to void settled bets, while a customer cannot cancel a bet once placed. In the Lukes case only state regulators stood between the customer and the loss of most of a win caused by the company’s error.',
    },
    {
      label: 'Friction and recourse',
      body: 'Funds are generally reachable quickly, but one regulator found a months-long unexplained hold. Recourse runs through 24/7 chat and email rather than a live phone line, with arbitration and a class-action waiver in the terms. In practice the strongest recourse has been state regulators rather than the company’s own processes.',
    },
    {
      label: 'Direction of the relationship',
      body: 'Mixed. Generosity to existing customers fell in 2024–2026 and loyalty terms tightened, while new-customer promotion, safety tooling and limit-notice rules improved. The relationship has not broadly deteriorated, but in specific places value has moved from customers to the company.',
    },
  ],
  unresolved: [
    'The investor transcripts and annual filings behind the reduced-promotion statements, the company’s own Illinois fee page and the 2024 shareholder letter could not be read in full. These control the two supported patterns (SP002 and SP004).',
    'The Michigan withdrawal order and the Massachusetts court’s *Scanlon* ruling were not read; their characterisation here rests on reporting.',
    'Operator-level data on how many DraftKings customers are limited, and how limiting interacts with promotions, are not public.',
    'Lawsuits over VIP hosts remain pending. Reporting in September 2026 about targeted promotions has not been tested by any regulator finding.',
  ],
  limitationsNote:
    'This investigation relied substantially on search-extracted material. Massachusetts, New Jersey and Connecticut regulatory documents, the Massachusetts house rules and the *De Leon* opinion were read in full; several company and investor documents were not reachable and are identified above. Quotations from those documents are attributed as reported.',
  sources: [
    {
      title: 'Decision: In the Matter of Crown MA Gaming, LLC d/b/a DraftKings Noncompliance Incident',
      publisher: 'Massachusetts Gaming Commission',
      date: '25 July 2025',
      url: 'https://massgaming.com/wp-content/uploads/DK-Noncompliance-Decision-Final-7.24.25.pdf',
      kind: 'Primary document',
    },
    {
      title: 'DraftKings Massachusetts Sportsbook House Rules, version 8.18.25 (implemented 26 August 2025)',
      publisher: 'DraftKings / Massachusetts Gaming Commission',
      date: '18 August 2025',
      url: 'https://massgaming.com/wp-content/uploads/DraftKings-House-Rules-8.18.25.pdf',
      kind: 'Primary document',
    },
    {
      title: 'DraftKings Massachusetts Sportsbook House Rules, version 6.1.23',
      publisher: 'DraftKings / Massachusetts Gaming Commission',
      date: '1 June 2023',
      url: 'https://massgaming.com/wp-content/uploads/DraftKings-House-Rules-6.1.23.pdf',
      kind: 'Primary document',
    },
    {
      title: 'Staff memo, “DraftKings Request to Void Wagers” (meeting materials)',
      publisher: 'Massachusetts Gaming Commission',
      date: '18 December 2025',
      url: 'https://massgaming.com/wp-content/uploads/Meeting-Materials-12.18.25-OPEN.pdf',
      kind: 'Primary document',
    },
    {
      title: 'Meeting minutes, 18 December 2025 (DraftKings void request)',
      publisher: 'Massachusetts Gaming Commission',
      date: '18 December 2025',
      url: 'https://massgaming.com/wp-content/uploads/Meeting-Minutes-12.18.25-OPEN.pdf',
      kind: 'Primary document',
    },
    {
      title: 'De Leon v. DraftKings, Inc., No. 25cv644 (DLC), Opinion and Order',
      publisher: 'U.S. District Court, Southern District of New York',
      date: '11 December 2025',
      url: 'https://storage.courtlistener.com/recap/gov.uscourts.nysd.635491/gov.uscourts.nysd.635491.70.0.pdf',
      kind: 'Primary document',
    },
    {
      title: 'Order, DGE v. Crown NJ Gaming, Inc. d/b/a DraftKings (self-excluded account)',
      publisher: 'New Jersey Division of Gaming Enforcement',
      date: 'October 2023',
      url: 'https://nj.gov/oag/ge/docs/Rulings/2023/oct16_31/B9draftkingsself.pdf',
      kind: 'Primary document',
    },
    {
      title: 'Assurance of Voluntary Compliance, In the Matter of Crown NJ Gaming Inc., DBA DraftKings (casino offers)',
      publisher: 'Connecticut Department of Consumer Protection',
      date: '7 July 2025',
      url: 'https://portal.ct.gov/dcp/-/media/dcp/gaming/pdfs/final-avc-draft-kings-2025.pdf',
      kind: 'Primary document',
    },
    {
      title: 'DraftKings Sportsbook Terms of Use — Massachusetts',
      publisher: 'DraftKings',
      date: '20 March 2026',
      url: 'https://sportsbook.draftkings.com/legal/ma-terms-of-use',
      kind: 'Primary document',
    },
    {
      title: 'DraftKings Q2 2024 Shareholder Letter (gaming tax surcharge)',
      publisher: 'DraftKings via SEC Form 8-K',
      date: '1 August 2024',
      url: 'https://www.sec.gov/Archives/edgar/data/1883685/000188368524000025/q224-prx8kexx991.htm',
      kind: 'Reported',
    },
    {
      title: '“DraftKings to Introduce Transaction Fee in Illinois”',
      publisher: 'DraftKings',
      date: '12 June 2025',
      url: 'https://draftkings.gcs-web.com/news-releases/news-release-details/draftkings-introduce-transaction-fee-illinois',
      kind: 'Reported',
    },
    {
      title: 'DraftKings Q3 2024 earnings call transcript',
      publisher: 'The Motley Fool',
      date: '8 November 2024',
      url: 'https://www.fool.com/earnings/call-transcripts/2024/11/08/draftkings-dkng-q3-2024-earnings-call-transcript/',
      kind: 'Reported',
    },
    {
      title: 'DraftKings fined in Michigan for not processing a player withdrawal',
      publisher: 'GamblingHarm.org (regulator records obtained by request)',
      date: 'June 2025',
      url: 'https://gamblingharm.org/draftkings-fined-in-michigan-for-not-processing-player-withdrawal/',
      kind: 'Reported',
    },
  ],
  methodology: [
    'CHI tested the hostile thesis and the null hypothesis category by category: business model, pricing, promotions, withdrawals, limiting, VIP treatment, responsible gambling, support, settlement rules, account enforcement, product design, regulatory history, loyalty and tax pass-through.',
    'Findings separate company policy from state legal requirements, current rules from superseded ones, and allegations from findings. Settlements are not treated as admissions. Customer reports were used only to identify patterns, never as proof.',
    'Semantic patterns SP001–SP004 were adjudicated under the CHI Semantic Pattern Taxonomy v1.0, counting each event once. An independent falsification pass and an adversarial verification pass preceded the final disposition.',
  ],
};