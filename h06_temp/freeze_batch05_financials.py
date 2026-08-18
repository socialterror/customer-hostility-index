import csv,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'; OUT=ROOT/'t0_scoring'; OUT.mkdir(exist_ok=True)
# F5 predictor calls, made only from frozen F1-F5 packets/reviews.
C={
63:('No Signal','N/A','LOW','NO','N/A','No qualifying customer-economic pricing or fee mechanism is established at F5; retrieved references are risk/accounting/customer-position noise.'),
64:('No Signal','N/A','LOW','NO','N/A','Client spreads and fees describe ordinary market-making economics rather than a new or intensified customer-yield mechanism at F5.'),
65:('SP002','Strong','HIGH','NO','Policyholders','Renewal/premium price increases are explicit from F1 and continue through F5, including implemented group long-term disability rate increases; strong but pre-existing.'),
66:('No Signal','N/A','LOW','NO','N/A','Cross-selling is described generically, while unauthorized-account litigation is not a company-originated qualifying yield action.'),
67:('No Signal','N/A','LOW','NO','N/A','Fees and commissions are ordinary revenue categories; the frozen F5 filing does not establish a qualifying new or intensified customer-economic mechanism.'),
68:('No Signal','N/A','LOW','NO','N/A','Commission and fee growth is reported, but the evidence does not establish a specific company-originated pricing/packaging action at F5.'),
69:('SP002','Strong','HIGH','NO','Long-term-care policyholders','Approved/expected premium rate increases and benefit reductions are explicit already at F1 and remain part of the LTC economics at F5; high intensity but static.'),
70:('No Signal','N/A','LOW','NO','N/A','The salient 2019 pricing action eliminated online trading commissions and reduced customer charges; this is opposite-direction to SP002 yield extraction and does not qualify.'),
71:('No Signal','N/A','LOW','NO','N/A','Regulatory Section 31 pass-through charges appear mid-window, but no sufficiently specific qualifying F5 customer-yield action is established.'),
72:('SP004','Strong','HIGH','NO','Insurance and packaging customers','Resin-price changes are contractually passed through to packaging customers from F1, while CNA also reports rate increases; customer cost-transfer is explicit and persistent rather than accelerating.'),
73:('No Signal','N/A','LOW','NO','N/A','Processing expenses, sales commissions and merchant/customer servicing costs do not establish a qualifying customer-facing pricing action at F5.'),
74:('No Signal','N/A','LOW','NO','N/A','No specific qualifying F5 customer pricing, entitlement, migration or cost-transfer mechanism is established.'),
75:('No Signal','N/A','LOW','NO','N/A','The retrieved fee/surcharge references are institutional expense items or non-customer mechanics rather than a qualifying F5 action.'),
76:('No Signal','N/A','LOW','NO','N/A','Inflation and claims-cost discussion is not explicitly linked to a customer premium/rate action in the frozen F5 filing.'),
77:('No Signal','N/A','LOW','NO','N/A','Transaction economics and protection losses are core operating mechanics; no specific qualifying new customer-yield action is established at F5.'),
78:('No Signal','N/A','LOW','NO','N/A','The frozen evidence is dominated by banking-rate/accounting mechanics and does not establish a qualifying F5 customer-economic action.'),
79:('No Signal','N/A','LOW','NO','N/A','Interchange/no-surcharge litigation describes longstanding network rules and allegations, not a new or intensified company-originated F5 yield action.'),
80:('No Signal','N/A','LOW','NO','N/A','F5 customer accommodations include deferred rate increases, fee waivers and premium credits; these are opposite-direction/customer-favorable and do not qualify.'),
81:('SP002','Strong','HIGH','NO','Life-insurance customers','Product design and pricing actions are already implemented at F1; F5 reports sales ahead of an August 2020 pricing increase. Specific and commercial, but the same pricing mechanism is pre-existing.'),
82:('No Signal','N/A','LOW','NO','N/A','Loan/deposit yields largely reflect prevailing interest-rate conditions; no qualifying F5 customer-yield mechanism is established.'),
83:('No Signal','N/A','LOW','NO','N/A','Client platform migration may affect FIS revenue depending on which system survives, but it is customer-led consolidation rather than a company-originated qualifying migration mechanism.'),
84:('No Signal','N/A','LOW','NO','N/A','Administrative and other fee revenues are reported as existing contract economics without a qualifying F5 pricing/packaging action.'),
85:('SP002','Strong','HIGH','NO','Lender-placed insurance policyholders/clients','Premium rate increases in lender-placed insurance are explicit at F1 and continue to contribute at F5; persistent implemented pricing rather than acceleration.'),
86:('SP002','Strong','HIGH','YES','Dealer clients','F1 shows dealers migrating away from monthly distribution-fee plans to all-variable plans; by F4/F5 the direction reverses and dealers migrate into plans incorporating a monthly distribution fee, explicitly increasing distribution-fee revenue. This is a material strengthening of customer-yield structure.'),
87:('No Signal','N/A','LOW','NO','N/A','No qualifying F5 customer pricing, entitlement, migration or cost-transfer mechanism is established.'),
88:('No Signal','N/A','LOW','NO','N/A','Premium/loss and inflation references are insurance operating economics without a specific qualifying F5 customer action.'),
89:('No Signal','N/A','LOW','NO','N/A','Deposit/loan pricing assumptions and transaction fees are ordinary banking mechanics; no specific qualifying F5 yield action is established.'),
90:('No Signal','N/A','LOW','NO','N/A','EMV migration litigation concerns alleged fraud-liability allocation rather than a current company-originated qualifying F5 economic action.'),
91:('No Signal','N/A','LOW','NO','N/A','Capital surcharges and service-fee revenue categories do not establish a qualifying customer-facing F5 pricing action.'),
92:('No Signal','N/A','LOW','NO','N/A','No qualifying F5 customer pricing, entitlement, migration or cost-transfer mechanism is established.'),
93:('No Signal','N/A','LOW','NO','N/A','Earlier regulatory discussion contemplates premium-rate approvals, but the frozen F5 filing does not establish a sufficiently specific qualifying action.'),
94:('No Signal','N/A','LOW','NO','N/A','Inflation and valuation assumptions are non-customer accounting/economic mechanics; no qualifying F5 action.'),
95:('No Signal','N/A','LOW','NO','N/A','FDIC surcharge references are bank regulatory costs, not customer charges, and no qualifying F5 action is established.'),
96:('No Signal','N/A','LOW','NO','N/A','An account-servicing fee increase is explicit at F1, but the frozen F5 evidence does not sustain a qualifying customer-yield signal; no acceleration.'),
97:('No Signal','N/A','LOW','NO','N/A','Advisory/administrative service fees describe the standing business model without a qualifying new or intensified F5 customer-economic action.'),
98:('No Signal','N/A','LOW','NO','N/A','Section 31 fees are regulatory pass-through charges; they do not rise above Moderate and are not a company-originated yield-optimization action at F5.')}
# Filing-level exceptions retained where useful to preserve trajectory.
EX={}
def fill(o, fps, cls,strength,state,actor,origin,spec,nov,persist,comm):
 for fp in fps: EX[(o,fp)]=(cls,strength,state,actor,origin,spec,nov,persist,comm)
fill(65,['F1','F2','F3','F4','F5'],'SP002','Strong','IMPLEMENTATION','Policyholders','Company-originated commercial model','High','Pre-existing','Persistent','High')
fill(69,['F1','F2','F3','F4','F5'],'SP002','Strong','IMPLEMENTATION','Long-term-care policyholders','Company-originated commercial model','High','Pre-existing','Persistent','High')
fill(72,['F1','F2','F3','F4','F5'],'SP004','Strong','IMPLEMENTATION','Insurance and packaging customers','Company-originated commercial model','High','Pre-existing','Persistent','High')
fill(81,['F1','F2','F3','F4','F5'],'SP002','Strong','IMPLEMENTATION','Life-insurance customers','Company-originated commercial model','High','Pre-existing','Persistent','High')
fill(85,['F1','F2','F3','F4','F5'],'SP002','Strong','IMPLEMENTATION','Lender-placed insurance policyholders/clients','Company-originated commercial model','High','Pre-existing','Persistent','High')
fill(86,['F1','F2','F3'],'No Signal','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A')
fill(86,['F4','F5'],'SP002','Strong','IMPLEMENTATION','Dealer clients','Company-originated commercial model','High','Increasing','Emerging','High')
fill(71,['F3'],'SP002','Moderate','IMPLEMENTATION','Exchange customers','Regulatory pass-through model','Moderate','Pre-existing','Isolated','Moderate')
fill(96,['F1'],'SP002','Strong','IMPLEMENTATION','Bank sweep/account clients','Company-originated commercial model','High','Pre-existing','Isolated','High')
fill(98,['F1','F2','F3','F4'],'SP002','Moderate','IMPLEMENTATION','Exchange customers','Regulatory pass-through model','Moderate','Pre-existing','Persistent','Moderate')
rows=[]
with MAN.open(newline='',encoding='utf-8') as f:
 for r in csv.DictReader(f):
  o=int(r['sample_order'])
  if 63<=o<=98: rows.append(r)
assert len(rows)==180
sig_fields=['sample_order','sector','ticker','company_name','CIK','filing_position','form','filing_date','accession_number','sec_locator','classification','signal_strength','temporal_state','affected_actor','origin_status','evidence_summary','specificity','novelty','persistence','commercial_explicitness','scorer_confidence']
sig=OUT/'H06_T0_SIGNAL_LEDGER_WORKING_BATCH05_FINANCIALS.csv'
with sig.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=sig_fields); w.writeheader()
 for r in rows:
  o=int(r['sample_order']); fp=r['filing_position']; pred=C[o]
  e=EX.get((o,fp),('No Signal','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'))
  out={k:r[k] for k in sig_fields[:10]}; out.update(dict(classification=e[0],signal_strength=e[1],temporal_state=e[2],affected_actor=e[3],origin_status=e[4],evidence_summary=pred[5],specificity=e[5],novelty=e[6],persistence=e[7],commercial_explicitness=e[8],scorer_confidence='High'))
  w.writerow(out)
cf=['sample_order','sector','ticker','company_name','F5_class','F5_strength','H06_intensity_binary','semantic_acceleration','affected_actor','trajectory_rationale','scorer_confidence','batch_status']
cp=OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH05_FROZEN.csv'; by={int(r['sample_order']):r for r in rows}
with cp.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=cf); w.writeheader()
 for o in range(63,99):
  r=by[o]; p=C[o]; w.writerow(dict(sample_order=o,sector='financials',ticker=r['ticker'],company_name=r['company_name'],F5_class=p[0],F5_strength=p[1],H06_intensity_binary=p[2],semantic_acceleration=p[3],affected_actor=p[4],trajectory_rationale=p[5],scorer_confidence='High',batch_status='FROZEN_WITHIN_BATCH_PRE_OUTCOME'))
high=sum(1 for p in C.values() if p[2]=='HIGH'); ay=sum(1 for p in C.values() if p[3]=='YES')
status={'companies':36,'filings':180,'high':high,'low':36-high,'acceleration_yes':ay,'acceleration_no':36-ay}
st=OUT/'batch05_status.json'; st.write_text(json.dumps(status,indent=2)+'\n')
note=OUT/'H06_T0_BATCH05_FREEZE_NOTE.md'; note.write_text(f'''# H06 T0 Batch 05 Freeze Note — Financials\n\nStatus: **FROZEN WITHIN BATCH — PRE-OUTCOME**\n\n- Sample orders: 063–098\n- Companies: 36\n- Frozen filings: 180\n- High Signal Intensity at F5: {high}\n- Low Signal Intensity at F5: {36-high}\n- Semantic Acceleration YES: {ay}\n- Semantic Acceleration NO: {36-ay}\n\nFinancial-market rates, accounting yields, regulatory capital surcharges, and ordinary fee-revenue labels were not treated as qualifying customer-economic actions without a specific company-originated mechanism. Customer-favorable fee reductions were also excluded from SP002.\n\nNo post-F5 outcome information was accessed or used.\n''')
cks=OUT/'H06_T0_BATCH05_CHECKSUMS.txt'; paths=[sig,cp,st,note]; cks.write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}' for p in paths)+'\n')
print(json.dumps(status))