import type { Investigation } from '@/lib/investigation-types';

// Source of truth: chi-research/fanduel/final-deliverables (master dossier, SP001–SP004,
// timeline, source ledger, verification memo), date of record 6 October 2026.
// Publication status: PUBLICATION READY WITH DISCLOSED LIMITATIONS. Required disclosure: the page
// must not state that sportsbook customers are charged the $2.99 inactivity fee.
export const fanduel: Investigation = {
  slug: 'fanduel',
  name: 'FanDuel',
  sectorSlug: 'gambling',
  status: 'published',
  investigationLabel: 'U.S. online sportsbook · customer-economics investigation',
  dateOfRecord: '6 October 2026',
  disposition: 'PARTIALLY SUPPORTS',
  dispositionNote: 'Lower end of the band, close to its lower boundary',
  summary:
    'FanDuel’s visible terms are good: competitive prices, fast and reachable payouts, and well-used safety tools. Value moves in the less visible places — a flat per-bet fee passed on from an Illinois tax, a free protection feature replaced by a paid one, discretionary limits and re-settlement rights, and responsible-gambling controls that have failed at scale at least once.',
  why: {
    paragraphs: [
      'FanDuel, owned by Flutter Entertainment, is the largest U.S. online sportsbook. CHI did not select it because of any prior finding against it. Its public record carried strong signals in both directions.',
      'On one side, it disclosed a margin strategy built on parlay products. In 2025 it became the first operator to charge customers a per-bet fee in Illinois. It acknowledged to regulators that it limits some skilled bettors, and it faced lawsuits and congressional letters about its VIP hosts. On the other side were market-leading prices on the available data, repeated industry awards and widely used spend-tracking tools.',
    ],
    thesis:
      'FanDuel’s U.S. sportsbook shows recurring, evidence-based patterns of customer extraction, asymmetry, access friction, winner limitation, withdrawal friction, promotional manipulation, value deterioration, recourse weakness, or product and enforcement design that shifts risk or cost onto customers.',
    nullHypothesis:
      'FanDuel offers a reasonably competitive product whose pricing, promotions, risk controls, account restrictions, responsible-gambling systems and customer-service procedures are proportionate to the value it delivers and to the regulatory obligations of a large sportsbook.',
  },
  executive: [
    'The evidence partially supports the hostile thesis, at the lower end of that band and close to its lower boundary.',
    'Three current mechanisms are documented by the company or a regulator: the Illinois per-bet fee; responsible-gambling controls that failed in Iowa and were penalised there and in four other states; and the replacement, in most states, of free injury protection on player-prop bets with a paid 3% add-on. Discretionary limits, re-settlement rights and promotion headlines that exceed realisable value add to the picture without being dramatic.',
    'None of these is systematic across the relationship, and all are offset by established counterevidence. FanDuel refused a tax surcharge in 2024, paid rather than voided in its documented settlement disputes, raised promotional generosity in 2025–2026, and has no adjudicated finding of deception against it.',
  ],
  findings: [
    {
      title: 'A flat per-bet fee passed on from the Illinois wagering tax',
      fact:
        'On 10 June 2025 FanDuel became the first operator to announce a $0.50 transaction fee on every online bet in Illinois, effective 1 September 2025.',
      evidence:
        'Flutter’s announcement tied the fee to “the significant increase in the cost of operating in Illinois driven by the new Illinois Transaction Fee” and promised to remove it if the state reversed course. The company expected it to recover about $30 million of a $35 million state cost in 2025. The fee was waived for about ten weeks in spring 2026; FanDuel’s help page, updated 5 October 2026, still describes a flat $0.50 on each bet. These documents were read in full.',
      implication:
        'An external tax was moved explicitly onto customers. A flat charge weighs most on small bets: 10% of a $5 stake, 1% of a $50 stake. Ten months earlier FanDuel had publicly refused to follow a rival’s surcharge on winnings.',
    },
    {
      title: 'Self-exclusion and limit-tool failures, worst in Iowa',
      fact:
        'For most of 2024, FanDuel customers in Iowa who chose lifetime self-exclusion were not properly excluded.',
      evidence:
        'Iowa’s regulator imposed $125,000 in July 2025 across five counts, including a responsible-gambling count. Its minutes record that the defect was fixed two days after discovery but the regulator was not told for 64 days. Trade reports put the affected group at 98 people, more than 30 of whom kept betting about $480,000. Iowa had already sanctioned FanDuel for self-exclusion failures in January 2024, and in July 2026 warned that further violations could put its licence at risk. Indiana, Virginia, New Jersey and Maryland have also penalised FanDuel for responsible-gambling control failures.',
      implication:
        'FanDuel’s safety tools are widely used, but they have failed at scale at least once, and the regulator learned of it late. It is the most serious responsible-gambling failure in FanDuel’s record.',
    },
    {
      title: 'Free injury protection replaced by a paid add-on in most states',
      fact:
        'In September 2025 FanDuel introduced Bet Protect, a free refund in bonus bets on NFL player-prop bets when the player is injured early in the game. It withdrew the feature for the 2026 playoffs.',
      evidence:
        'From April 2026 it offers Bet Protect+, an optional add-on costing 3% of the stake, which covers the full game and refunds straight bets in cash. Its current help article says the free Bet Protect is offered only “in states where Bet Protect+ is not available” — Connecticut, Massachusetts and Tennessee, where it remains a standing feature.',
      implication:
        'Where the paid product is approved, a protection customers received free now costs 3%. The paid version is broader and pays cash, and the free one was new and seasonal, which is why CHI treats this as a weak rather than strong instance.',
    },
    {
      title: 'A margin strategy built on parlays',
      fact:
        'Flutter told investors in 2024 that its parlay products mean “FanDuel extracts more commercial value from those players”.',
      evidence:
        'It reports a structural sportsbook margin of 14.2% for 2025, targets 16% over the long term and attributes gains to its parlay offering. Bank data for Illinois showed parlays as about 64% of FanDuel’s handle. Its app places popular parlays on the home screen and live same-game parlays in play.',
      implication:
        'Higher parlay margins are ordinary sportsbook economics, and customers choose these products. The CHI concern is the combination of a stated aim to raise per-customer value with design that puts the highest-margin products first.',
    },
    {
      title: 'Discretionary limits and after-the-fact settlement rights',
      fact:
        'FanDuel’s Massachusetts house rules reserve the right “to set a lower or higher maximum bet wager amount per customer”. They also allow it to reverse any settlement made in error, including cash-outs, with no general time limit.',
      evidence:
        'At a 2024 regulator roundtable FanDuel described reviewing customers by the markets they bet, their wager types and their outcomes. A 48-hour correction window applies only to results set without an official source; official results stand even if later amended. Customers cannot cancel a placed bet. Outside Massachusetts, which has required reasoned notice since June 2026, limits need no stated reason.',
      implication:
        'Limiting skilled bettors is common practice and affects a small share of activity. The asymmetry is that FanDuel can restrict and re-settle while the customer cannot cancel, softened where the rules favour the customer — for example, settling correlated parlays as singles rather than voiding them.',
    },
  ],
  counterevidence: [
    {
      title: 'It refused to pass a tax on to winners',
      body: 'In August 2024 FanDuel publicly said it had “no plans to introduce a surcharge for winners”, after a rival announced one for four high-tax states; the rival withdrew its plan within an hour of that statement. FanDuel also absorbed Illinois’ 2024 tax increase before the 2025 per-wager levy.',
    },
    {
      title: 'Prices and awards',
      body: 'On the only third-party pricing dataset found (2024), FanDuel had the market’s lowest margins; later comparisons are mixed. It was named sportsbook operator of the year by a major industry body four years running.',
    },
    {
      title: 'Customers can reach their money',
      body: 'FanDuel publishes its withdrawal review window, pays e-wallet withdrawals within 24 hours, publishes a route for refunding unused deposits and charges no deposit or withdrawal fees. It excludes credit cards from sportsbook deposits in every state by its own policy.',
    },
    {
      title: 'It paid in documented settlement disputes',
      body: 'In every documented settlement dispute since 2022 it paid rather than voided, including a home-run parlay that paid $100,276 on an $11 bonus bet; copycat bets on the same parlay were reported to cost far more. It refunded Indiana customers whose self-set limits it failed to enforce, and extended lifetime exclusion to everyone affected by the Iowa defect.',
    },
    {
      title: 'Widely used safety tools',
      body: 'Its My Spend tool was used by about 3.5 million customers in the 2024–25 NFL season, and it runs real-time behavioural check-ins. Its parent publishes a target for responsible-gambling tool adoption.',
    },
    {
      title: 'Rising generosity and a small, mostly operational penalty record',
      body: 'Promotional spend as a share of handle rose through 2025 and 2026, and management said openly that it had pulled back too far. Its regulatory penalties total about $591,000 across 23 matters, about 0.008% of one year’s U.S. revenue, and are mostly operational. No regulator has found its promotions deceptive.',
    },
    {
      title: 'No adverse court ruling',
      body: 'No court has ruled against FanDuel on the merits. The one VIP-host suit to reach a ruling was sent to arbitration; the others are pending.',
    },
  ],
  patterns: [
    {
      id: 'SP001',
      name: 'Unmonetized Access / Entitlement Monetization',
      verdict: 'WEAKLY SUPPORTED',
      confidence: 'Medium',
      explanation:
        'In states where Bet Protect+ is approved, free injury protection on player props was replaced by a paid 3% add-on: a previously included feature moved behind payment. It is weak because the free feature was about seven months old, seasonal and paid in bonus bets. The paid version is broader, and the free one continues as a standing feature in Connecticut, Massachusetts and Tennessee.',
    },
    {
      id: 'SP002',
      name: 'Existing-Customer Yield Optimization',
      verdict: 'WEAKLY SUPPORTED',
      confidence: 'Medium',
      explanation:
        'FanDuel’s Terms introduced a $2.99 monthly fee on accounts inactive for 24 months in 2019, and customers were notified of it in January 2025. CHI could not read the current Terms. The support article that described the fee has since been retired, and it is unverified whether the fee is still applied or reaches sportsbook balances. CHI does not find that sportsbook customers are charged it.',
    },
    {
      id: 'SP003',
      name: 'Legacy Product Deprioritization / Portfolio Concentration',
      verdict: 'INSUFFICIENT EVIDENCE',
      confidence: 'Low',
      explanation:
        'A reported platform migration around 2020 locked some customers out, but its date, scope and consequences could not be established. No other legacy product was retired with forced migration.',
    },
    {
      id: 'SP004',
      name: 'Cost Pressure → Customer Cost Transfer',
      verdict: 'SUPPORTED',
      confidence: 'Medium-High',
      explanation:
        'The Illinois $0.50 per-bet fee explicitly passes the state’s per-wager tax to customers, with a stated commitment to remove it if the tax is reversed. FanDuel’s current help page describes it as a flat charge on each bet.',
    },
  ],
  timeline: [
    {
      period: '2018–2023: risk-free offers and early enforcement',
      body: 'FanDuel’s early welcome offers were large refund-style “risk-free” and No Sweat bets, worth far less than their headlines to a typical customer. In 2019 its Terms introduced a monthly fee on long-inactive accounts. Regulators in Virginia, New Jersey, Indiana and Maryland penalised it in 2021–2023 for operational and responsible-gambling control failures.',
    },
    {
      period: '2024: limiting scrutiny, Iowa and a refused surcharge',
      body: 'Iowa sanctioned FanDuel twice in January 2024 for self-exclusion failures. During 2024 its lifetime self-exclusion option in Iowa stopped working. In August it refused to follow a rival’s winnings surcharge, and in September it described its limiting practice at a Massachusetts regulator roundtable. Welcome offers became conditional on the first bet winning.',
    },
    {
      period: '2025: the Illinois fee and free Bet Protect',
      body: 'In June FanDuel announced the Illinois per-bet fee, live from 1 September. In July Iowa imposed $125,000, including for the self-exclusion defect, and Indiana penalised failures to enforce self-set limits. In September FanDuel introduced free Bet Protect on NFL player props.',
    },
    {
      period: '2026: paid protection, a fee waiver and more generosity',
      body: 'Free Bet Protect was withdrawn for the playoffs, and from April the paid 3% Bet Protect+ took its place where approved. The Illinois fee was waived for about ten weeks in spring; the company’s help page now describes it as in force. Massachusetts began requiring reasoned notice of betting limits in June. In July Iowa warned FanDuel about its licence after further violations. Promotional generosity rose, and FanDuel launched a sportsbook rewards club in September with no published cash value for its points. Congressional letters questioned its VIP programme.',
    },
  ],
  meaning: [
    {
      label: 'Customer value',
      body: 'The price of the core product is fair on the available evidence, the money is reachable, and safety tools are widely used. For most customers the relationship is a competitive one.',
    },
    {
      label: 'Extraction',
      body: 'Extraction is concentrated and explicit: a flat fee passed on from a state tax, a free protection turned into a paid one where approved, and a margin strategy that favours parlays. It is not hidden, but it sits below the headline terms.',
    },
    {
      label: 'Asymmetry',
      body: 'FanDuel can limit skilled bettors and reverse settlements made in error; customers cannot cancel a bet. Some rules lean the customer’s way — official results stand, correlated parlays settle as singles — so the asymmetry is real but moderated.',
    },
    {
      label: 'Friction and recourse',
      body: 'Withdrawal friction is low. Recourse relies on chat and callback support during set hours, an internal dispute step and state regulators, with arbitration in the terms. The VIP layer, where the most serious harm is alleged, is the part about which least is established.',
    },
    {
      label: 'Direction of the relationship',
      body: 'Mixed. New charges appeared in 2025–2026 — the Illinois fee and the paid Bet Protect+ — while generosity rose and prices stayed competitive. The places to watch are the parlay the app suggests, the condition beneath a promotion’s headline, the per-bet charge in Illinois and the settlement fine print.',
    },
  ],
  unresolved: [
    'Whether the $2.99 inactivity fee in FanDuel’s Terms is still applied, and whether it has ever reached a sportsbook balance. The current Terms could not be read and the support article describing the fee has been retired. This could change one pattern verdict (SP002) but not the overall disposition on its own.',
    'Whether the Illinois fee was formally reinstated after the spring 2026 waiver; the company’s current help page describes it as in force, but no reinstatement notice was found.',
    'How FanDuel’s VIP hosts are paid, and how the pending VIP lawsuits and a reported Pennsylvania review will end.',
    'Whether a limited account also loses promotional eligibility, and how FanDuel’s limiting compares with the market at operator level.',
    'The Maryland, Indiana and Virginia orders, and the regulator documents behind the Iowa cohort figures, were not read in full.',
  ],
  limitationsNote:
    'Published with disclosed limitations. The decisive documents — FanDuel’s support articles on the Illinois fee and Bet Protect, Flutter’s announcements and investor materials, the Massachusetts house rules and the Iowa, New Jersey and Massachusetts regulators’ records — were read in full. FanDuel’s Terms of Use could not be reached, so the inactivity-fee question remains open and is described only as unresolved.',
  sources: [
    {
      title: '“Flutter response to Illinois Transaction Fee”',
      publisher: 'Flutter Entertainment plc',
      date: '10 June 2025',
      url: 'https://flutter.com/news-and-insights/press-releases/flutter-response-to-illinois-transaction-fee/',
      kind: 'Primary document',
    },
    {
      title: '“FanDuel in Illinois” (support article)',
      publisher: 'FanDuel',
      date: 'Last published 5 October 2026',
      url: 'https://support.fanduel.com/s/article/FanDuel-in-Illinois',
      kind: 'Primary document',
    },
    {
      title: '“FanDuel’s Bet Protect+ and Bet Protect” (support article)',
      publisher: 'FanDuel',
      date: 'Last published 6 October 2026',
      url: 'https://support.fanduel.com/s/article/Bet-Protect-with-FanDuel',
      kind: 'Primary document',
    },
    {
      title: 'FanDuel Sportsbook House Rules (Massachusetts), version 7.30.26',
      publisher: 'FanDuel / Massachusetts Gaming Commission',
      date: '30 July 2026',
      url: 'https://massgaming.com/wp-content/uploads/FanDuel-House-Rules-7.30.26.pdf',
      kind: 'Primary document',
    },
    {
      title: 'Meeting minutes, 11 September 2024 (limiting roundtable)',
      publisher: 'Massachusetts Gaming Commission',
      date: '11 September 2024',
      url: 'https://massgaming.com/wp-content/uploads/Meeting-Minutes-9.11.24-OPEN.pdf',
      kind: 'Primary document',
    },
    {
      title: 'Commission minutes, 11 July 2025 (FanDuel penalties)',
      publisher: 'Iowa Racing and Gaming Commission',
      date: '11 July 2025',
      url: 'https://irgc.iowa.gov/media/461/download?inline',
      kind: 'Primary document',
    },
    {
      title: 'Commission minutes, 25 January 2024 (self-exclusion stipulations)',
      publisher: 'Iowa Racing and Gaming Commission',
      date: '25 January 2024',
      url: 'https://irgc.iowa.gov/media/388/download?inline',
      kind: 'Primary document',
    },
    {
      title: 'Commission minutes, 24 July 2026 (impermissible wagers; licence warning)',
      publisher: 'Iowa Racing and Gaming Commission',
      date: '24 July 2026',
      url: 'https://irgc.iowa.gov/media/512/download?inline',
      kind: 'Primary document',
    },
    {
      title: 'Flutter Q4 and full-year 2025 earnings release',
      publisher: 'Flutter Entertainment plc',
      date: '26 February 2026',
      url: 'https://flutter.com/media/hdshhrmb/q4-2025-earnings-release.pdf',
      kind: 'Primary document',
    },
    {
      title: '“Can I cancel a Sportsbook wager or bet?” (support article)',
      publisher: 'FanDuel',
      date: 'Last published 5 March 2024',
      url: 'https://support.fanduel.com/s/article/Can-I-Cancel-a-Wager-or-Bet',
      kind: 'Primary document',
    },
    {
      title: '“Do I have to pay any deposit or withdrawal fees on FanDuel?” (support article)',
      publisher: 'FanDuel',
      date: 'Last published 29 June 2026',
      url: 'https://support.fanduel.com/s/article/Do-I-have-to-pay-any-deposit-or-withdrawal-fees-on-FanDuel',
      kind: 'Primary document',
    },
    {
      title: '“FanDuel is now charging inactive users $3 per month”',
      publisher: 'TechCrunch',
      date: '1 May 2019',
      url: 'https://techcrunch.com/2019/05/01/fanduel-is-now-charging-inactive-users-3-per-month-for-not-playing/',
      kind: 'Reported',
    },
  ],
  methodology: [
    'CHI tested the hostile thesis and the null hypothesis category by category: business model, pricing, promotions, withdrawals, limiting, VIP treatment, responsible gambling, support, settlement rules, account enforcement, product design, regulatory history, loyalty and tax pass-through.',
    'Findings separate company policy from state legal requirements, current rules from superseded ones, and allegations from findings. Settlements are not treated as admissions. Customer reports were used only to identify patterns, never as proof.',
    'Semantic patterns SP001–SP004 were adjudicated under the CHI Semantic Pattern Taxonomy v1.0, counting each event once. An independent falsification pass, an adversarial verification pass and a primary-source verification pass preceded the final disposition.',
  ],
};