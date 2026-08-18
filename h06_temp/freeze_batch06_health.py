import csv,json,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'t0_scoring'; OUT.mkdir(exist_ok=True)
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
D={
99:('DHR','SP002','Strong','HIGH','NO','Laboratory/life-science customers','Segment price increases are already contributing to sales at F1 and remain an established pricing mechanism; high intensity but not accelerating.'),
100:('IQV','No Signal','N/A','LOW','NO','N/A','Fixed-price and migration references do not establish a qualifying customer-economic action.'),
101:('ABMD','No Signal','N/A','LOW','NO','N/A','No qualifying customer pricing, entitlement, migration, or cost-transfer mechanism is established.'),
102:('MDT','No Signal','N/A','LOW','NO','N/A','Derivative/reference-rate discontinuation language is accounting/financing rather than customer-product withdrawal.'),
103:('MCK','No Signal','N/A','LOW','NO','N/A','Drug price increases are described as market/industry growth rather than a company-originated customer action.'),
104:('REGN','No Signal','N/A','LOW','NO','N/A','Rebate and inflation language reflects statutory pricing rules and regulation, not a new company-originated customer action.'),
105:('ALGN','SP002','Strong','HIGH','NO','Clear-aligner customers','Higher ASP from price increases and mix is already explicit at F1 and persists; strong but static existing-customer yield optimization.'),
106:('ABBV','No Signal','N/A','LOW','NO','N/A','Pricing references are primarily regulatory-risk discussion rather than a concrete company action in the frozen trajectory.'),
107:('BIO','SP004','Moderate','LOW','NO','Laboratory/research customers','F5 explicitly links inflationary acquired-goods costs to attempted price recovery, but the language stresses inability/restriction and does not establish a Strong implemented transfer.'),
108:('CI','No Signal','N/A','LOW','NO','N/A','Higher branded-drug prices primarily reflect upstream drug-price inflation and customer-transition mechanics rather than a qualifying Cigna-originated action.'),
109:('VAR','No Signal','N/A','LOW','NO','N/A','Acquisition and LIBOR-migration language is non-qualifying.'),
110:('RMD','No Signal','N/A','LOW','NO','N/A','Share-repurchase and reference-rate discontinuation language does not affect customers.'),
111:('PKI','No Signal','N/A','LOW','NO','N/A','The filing describes inability to pass shipping cost increases to customers, not a qualifying implemented customer-cost transfer.'),
112:('PFE','No Signal','N/A','LOW','NO','N/A','Price-increase and rebate references are legislative/regulatory risk language, not a concrete company-originated action.'),
113:('BDX','No Signal','N/A','LOW','NO','N/A','Reimbursement and inflation discussion does not establish a qualifying customer-economic action.'),
114:('ZTS','No Signal','N/A','LOW','NO','N/A','Discontinuation references concern hedging/accounting rather than customer products.'),
115:('CVS','SP004','Moderate','LOW','NO','Insured health-plan members','Premium-rate increases are explicitly linked to rising health-care/benefit costs from F1 onward, but the frozen language remains regulatory/risk constrained rather than Strong implemented transfer.'),
116:('LH','SP002','Moderate','LOW','NO','Patients/third-party payers','Patient list-price fee schedules and negotiated discounts are an established pricing architecture, but no material strengthening or new mechanism appears by F5.'),
117:('HUM','No Signal','N/A','LOW','NO','N/A','Medicare Part D cost-sharing stages are statutory plan-design mechanics rather than a newly company-originated economic action.'),
118:('ALXN','SP002','Moderate','LOW','NO','Patients/payers','The company repeatedly describes higher-priced therapies and payer barriers, but the trajectory does not show a Strong new pricing action.'),
119:('UNH','No Signal','N/A','LOW','NO','N/A','Rate references are interest-rate/tax mechanics rather than customer pricing actions.'),
120:('COO','No Signal','N/A','LOW','NO','N/A','Rate-increase references concern indebtedness and financing, not customers.'),
121:('EW','SP003','Strong','HIGH','NO','TAVR customers','The decision to discontinue the CENTERA program is already explicit in the opening filing and remains the same portfolio-withdrawal mechanism through F5.'),
122:('ABC','No Signal','N/A','LOW','NO','N/A','Price increases are discussed as pharmaceutical-industry/regulatory conditions rather than an AmerisourceBergen-originated customer action.'),
123:('HOLX','No Signal','N/A','LOW','NO','N/A','Standalone selling-price and disposal accounting language does not establish a qualifying customer-economic action.'),
124:('ANTM','SP004','Very Strong','HIGH','NO','Health-plan members','Premium rate increases are explicitly designed to cover overall cost trends at F1 and remain so through F5; very strong but fully pre-existing.'),
125:('TFX','No Signal','N/A','LOW','NO','N/A','The company describes inability to pass higher costs to customers rather than an implemented transfer.'),
126:('ABT','No Signal','N/A','LOW','NO','N/A','Price/rebate references are policy and reimbursement risk language, not a concrete Abbott customer-economic action.')}
rows=list(csv.DictReader(MAN.open()))
company=[]; filings=[]
for order,(ticker,cls,strength,intensity,accel,actor,rat) in D.items():
    rr=[r for r in rows if int(r['sample_order'])==order]
    assert len(rr)==5
    name=rr[0]['company_name']
    company.append({'sample_order':order,'sector':'health_care','ticker':ticker,'company_name':name,'F5_class':cls,'F5_strength':strength,'H06_intensity_binary':intensity,'semantic_acceleration':accel,'affected_actor':actor,'trajectory_rationale':rat,'scorer_confidence':'High' if cls!='SP004' or ticker=='ANTM' else 'Moderate-High','batch_status':'FROZEN_WITHIN_BATCH_PRE_OUTCOME'})
    for r in rr:
        filings.append({**r,'classification':cls,'signal_strength':strength,'temporal_state':'IMPLEMENTATION' if cls not in ('No Signal','Neutral') else 'N/A','affected_actor':actor,'origin_status':'Company-originated commercial model' if cls not in ('No Signal','Neutral') else 'N/A','evidence_summary':rat,'specificity':'High' if strength in ('Strong','Very Strong') else ('Moderate' if strength=='Moderate' else 'N/A'),'novelty':'Pre-existing' if cls not in ('No Signal','Neutral') else 'N/A','persistence':'Persistent' if cls not in ('No Signal','Neutral') else 'None','commercial_explicitness':'High' if strength in ('Strong','Very Strong') else ('Moderate' if strength=='Moderate' else 'N/A'),'scorer_confidence':'High'})
cp=OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH06_FROZEN.csv'; fp=OUT/'H06_T0_SIGNAL_LEDGER_WORKING_BATCH06_HEALTH_CARE.csv'
for p,data in [(cp,company),(fp,filings)]:
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
h=sum(x['H06_intensity_binary']=='HIGH' for x in company); ay=sum(x['semantic_acceleration']=='YES' for x in company)
status={'companies':len(company),'filings':len(filings),'high':h,'low':len(company)-h,'acceleration_yes':ay,'acceleration_no':len(company)-ay}
(OUT/'batch06_status.json').write_text(json.dumps(status,indent=2)+'\n')
note=OUT/'H06_T0_BATCH06_FREEZE_NOTE.md'; note.write_text(f'# H06 Blind T0 Scoring — Batch 06 Freeze Note\n\nSector: Health Care\nCompanies: {len(company)}\nFilings: {len(filings)}\nHigh: {h}\nLow: {len(company)-h}\nAcceleration YES: {ay}\nAcceleration NO: {len(company)-ay}\n\nNo post-F5 outcome information was inspected or used.\n')
checks=OUT/'H06_T0_BATCH06_CHECKSUMS.txt'
with checks.open('w') as f:
    for p in (cp,fp,note): f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
print(status)
