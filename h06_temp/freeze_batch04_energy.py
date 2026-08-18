import csv, hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / 'output' / 'H06_SAMPLE_MANIFEST_FROZEN.csv'
OUT = ROOT / 't0_scoring'
OUT.mkdir(exist_ok=True)

FIELDS = ['sample_order','sector','ticker','company_name','CIK','filing_position','form','filing_date','accession_number','sec_locator','classification','signal_strength','temporal_state','affected_actor','origin_status','evidence_summary','specificity','novelty','persistence','commercial_explicitness','scorer_confidence']

COMPANY = {
52: dict(ticker='FANG', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Realized oil, gas and NGL prices are market-index commodity outcomes and hedging mechanics; the frozen filings do not establish a company-originated customer pricing, entitlement, migration or cost-transfer mechanism.'),
53: dict(ticker='NOV', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='The annual F2 filing discloses surcharges and price adjustments used to mitigate higher raw-material costs, but the mechanism is not sustained or materially strengthened through F5; F5 is dominated by customer capital-spending and commodity-market weakness.'),
54: dict(ticker='FTI', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Fixed-price project risk, customer demand and commodity-price exposure are discussed, but no qualifying company-originated customer-economic mechanism is established in the frozen F5 filing.'),
55: dict(ticker='APA', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Customer contracts use market-indexed commodity prices and market-reflective differentials; these are commodity-market mechanics rather than a qualifying company-originated customer yield or cost-transfer action.'),
56: dict(ticker='COP', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Long-term commodity sales use prevailing market prices and derivative activity manages commodity exposure; the frozen filings do not identify a qualifying company-originated customer-economic action.'),
57: dict(ticker='OXY', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Commodity-price derivatives, market-linked sales and asset-sale activity dominate the evidence; no qualifying customer pricing, entitlement, migration or cost-transfer mechanism is established at F5.'),
58: dict(ticker='KMI', f5='SP002', strength='Moderate', intensity='LOW', accel='NO', actor='Pipeline shippers', confidence='High', rationale='Indexed tariff/rate increases charged to shippers are explicit at F1 and remain explicit at F5, but the mechanism is regulated, contested and materially static rather than newly strengthening.'),
59: dict(ticker='HES', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Selling-price and midstream-tariff references primarily reflect commodity markets and operating economics; environmental/JDA cost-recovery references are not customer-economic actions.'),
60: dict(ticker='DVN', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='The apparent price changes are commodity-market movements and hedging results; divestitures and cost reductions do not create a qualifying customer-economic mechanism.'),
61: dict(ticker='BKR', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Customer spending and demand are linked to commodity prices, while derivatives hedge input costs; the frozen filings do not establish a qualifying company-originated pricing or cost-transfer action.'),
62: dict(ticker='PXD', f5='No Signal', strength='N/A', intensity='LOW', accel='NO', actor='N/A', confidence='High', rationale='Reported oil, NGL and gas prices are explicitly market prices received for commodities; derivative and transportation commitments do not constitute a qualifying company-originated customer-economic mechanism.'),
}

# Filing-specific exception(s). All unspecified Energy filings are No Signal except KMI's persistent regulated-rate mechanism.
FILING = {
    (53,'F2'): dict(classification='SP004', signal_strength='Moderate', temporal_state='IMPLEMENTATION', affected_actor='Equipment/service customers', origin_status='Company-originated commercial model', evidence_summary='NOV states it has generally mitigated higher raw-material costs by applying surcharges to and adjusting prices on products it sells.', specificity='Moderate', novelty='Pre-existing', persistence='Isolated', commercial_explicitness='Moderate', scorer_confidence='High'),
}
for fp in ['F1','F2','F3','F4','F5']:
    FILING[(58,fp)] = dict(classification='SP002', signal_strength='Moderate', temporal_state='IMPLEMENTATION', affected_actor='Pipeline shippers', origin_status='Regulated company-originated tariff/rate model', evidence_summary='Kinder Morgan/SFPP filings describe tariff and indexed rate increases charged to shippers and related regulatory challenges; the same mechanism persists without material strengthening.', specificity='Moderate', novelty='Pre-existing', persistence='Persistent', commercial_explicitness='Moderate', scorer_confidence='High')

rows = []
with MANIFEST.open(newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        o = int(r['sample_order'])
        if 52 <= o <= 62:
            rows.append(r)
assert len(rows) == 55, len(rows)

signal_path = OUT / 'H06_T0_SIGNAL_LEDGER_WORKING_BATCH04_ENERGY.csv'
with signal_path.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in rows:
        o = int(r['sample_order']); fp = r['filing_position']; c = COMPANY[o]
        s = FILING.get((o,fp), dict(classification='No Signal', signal_strength='N/A', temporal_state='N/A', affected_actor='N/A', origin_status='N/A', evidence_summary=c['rationale'], specificity='N/A', novelty='N/A', persistence='N/A', commercial_explicitness='N/A', scorer_confidence=c['confidence']))
        out = {k:r.get(k,'') for k in ['sample_order','sector','ticker','company_name','CIK','filing_position','form','filing_date','accession_number','sec_locator']}
        out.update(s)
        w.writerow(out)

company_fields = ['sample_order','sector','ticker','company_name','F5_class','F5_strength','H06_intensity_binary','semantic_acceleration','affected_actor','trajectory_rationale','scorer_confidence','batch_status']
company_path = OUT / 'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH04_FROZEN.csv'
seen = {}
for r in rows:
    seen[int(r['sample_order'])] = r
with company_path.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=company_fields); w.writeheader()
    for o in range(52,63):
        r=seen[o]; c=COMPANY[o]
        w.writerow(dict(sample_order=o, sector='energy', ticker=c['ticker'], company_name=r['company_name'], F5_class=c['f5'], F5_strength=c['strength'], H06_intensity_binary=c['intensity'], semantic_acceleration=c['accel'], affected_actor=c['actor'], trajectory_rationale=c['rationale'], scorer_confidence=c['confidence'], batch_status='FROZEN_WITHIN_BATCH_PRE_OUTCOME'))

status = {'companies':11,'filings':55,'high':0,'low':11,'acceleration_yes':0,'acceleration_no':11}
status_path = OUT / 'batch04_status.json'
status_path.write_text(json.dumps(status, indent=2)+'\n', encoding='utf-8')

note = '''# H06 T0 Batch 04 Freeze Note — Energy\n\nStatus: **FROZEN WITHIN BATCH — PRE-OUTCOME**\n\n- Sample orders: 052–062\n- Sector: Energy\n- Companies: 11\n- Frozen filings: 55\n- High Signal Intensity at F5: 0\n- Low Signal Intensity at F5: 11\n- Semantic Acceleration YES: 0\n- Semantic Acceleration NO: 11\n\n## Interpretation boundary\nThe dominant Energy-sector price language in this frozen window concerns externally determined commodity prices, hedging, reserve economics, and customer capital-spending sensitivity. Under the H06 taxonomy, market price movement by itself is not a company-originated customer-economic action.\n\nNOV contains a qualifying F2 cost-transfer disclosure (surcharges/price adjustments for raw-material costs), but it does not persist or strengthen into F5 and therefore does not produce High F5 intensity or acceleration. Kinder Morgan contains a persistent regulated SP002 tariff/rate mechanism, but it remains Moderate and static.\n\nNo post-F5 outcome information was accessed or used in these classifications.\n'''
note_path = OUT / 'H06_T0_BATCH04_FREEZE_NOTE.md'
note_path.write_text(note, encoding='utf-8')

checksum_path = OUT / 'H06_T0_BATCH04_CHECKSUMS.txt'
lines=[]
for p in [signal_path, company_path, status_path, note_path]:
    lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}")
checksum_path.write_text('\n'.join(lines)+'\n', encoding='utf-8')

print(json.dumps(status))