import csv, pathlib, hashlib, json
ROOT=pathlib.Path(__file__).resolve().parent
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
SCORES=ROOT/'t0_scoring'/'batch02_company_scores.csv'
OUT=ROOT/'t0_scoring'; OUT.mkdir(exist_ok=True)
score_rows=list(csv.DictReader(SCORES.open(encoding='utf-8')))
by_order={int(r['sample_order']):r for r in score_rows}
manifest=[r for r in csv.DictReader(MAN.open(encoding='utf-8')) if 10<=int(r['sample_order'])<=35]
if len(manifest)!=130: raise SystemExit(f'Expected 130 manifest rows, got {len(manifest)}')
filing=[]
for m in manifest:
    s=by_order[int(m['sample_order'])]; pos=m['filing_position']; cls=s[f'{pos}_class']; strength=s[f'{pos}_strength']
    temporal='N/A' if cls in ('No Signal','Neutral') else ('ANNOUNCED' if int(m['sample_order'])==10 and pos in ('F1','F2') else 'IMPLEMENTATION')
    filing.append({
      'sample_order':m['sample_order'],'sector':m['sector'],'ticker':m['ticker'],'company_name':m['company_name'],'CIK':m['CIK'],
      'filing_position':pos,'form':m['form'],'filing_date':m['filing_date'],'accession_number':m['accession_number'],'sec_locator':m['sec_locator'],
      'classification':cls,'signal_strength':strength,'temporal_state':temporal,
      'affected_actor':s['affected_actor'] if cls not in ('No Signal','Neutral') else 'N/A',
      'origin_status':'Company-originated commercial model' if cls not in ('No Signal','Neutral') else 'N/A',
      'evidence_summary':s['trajectory_rationale'],
      'specificity':'High' if strength in ('Strong','Very Strong') else ('Moderate' if strength=='Moderate' else ('Low' if strength=='Weak' else 'N/A')),
      'novelty':'Increasing' if s['semantic_acceleration']=='YES' and pos not in ('F1',) else ('Pre-existing' if cls not in ('No Signal','Neutral') else 'None'),
      'persistence':'Persistent' if cls not in ('No Signal','Neutral') and s['semantic_acceleration']=='NO' else ('Trajectory-dependent' if cls not in ('No Signal','Neutral') else 'None'),
      'commercial_explicitness':'High' if strength in ('Strong','Very Strong') else ('Moderate' if strength=='Moderate' else ('Low' if strength=='Weak' else 'N/A')),
      'scorer_confidence':s['scorer_confidence']
    })
filing_path=OUT/'H06_T0_SIGNAL_LEDGER_WORKING_BATCH02_CONSUMER_DISCRETIONARY.csv'
with filing_path.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=filing[0].keys()); w.writeheader(); w.writerows(filing)
company_fields=['sample_order','sector','ticker','company_name','F5_class','F5_strength','H06_intensity_binary','semantic_acceleration','affected_actor','trajectory_rationale','scorer_confidence']
company=[]
for s in score_rows:
    company.append({k:s[k] for k in company_fields})
cp=OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH02_FROZEN.csv'
with cp.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=company_fields+['batch_status']); w.writeheader()
    for r in company: w.writerow({**r,'batch_status':'FROZEN_WITHIN_BATCH_PRE_OUTCOME'})
high=sum(r['H06_intensity_binary']=='HIGH' for r in company); acc=sum(r['semantic_acceleration']=='YES' for r in company)
note=['# H06 Blind T0 Scoring — Batch 02 Freeze Note','','**Sector:** Consumer Discretionary  ','**Companies:** 26  ','**Filings:** 130  ','**Status:** FROZEN WITHIN BATCH — PRE-OUTCOME','','No post-F5 outcome information was inspected or used.','','## Company predictor calls','','| # | Ticker | F5 class | F5 strength | Intensity | Acceleration |','|---:|---|---|---|---|---|']
for r in company:
    note.append(f"| {r['sample_order']} | {r['ticker']} | {r['F5_class']} | {r['F5_strength']} | {r['H06_intensity_binary']} | {r['semantic_acceleration']} |")
note += ['', '## Batch totals','',f'- High Signal Intensity: {high}',f'- Low Signal Intensity: {26-high}',f'- Semantic Acceleration YES: {acc}',f'- Semantic Acceleration NO: {26-acc}','','### Acceleration YES cases']
for r in company:
    if r['semantic_acceleration']=='YES': note.append(f"- {r['ticker']}")
note += ['','These calls are frozen within Batch 02 before scoring later sectors. Later-company evidence may not be used to rewrite them.']
np=OUT/'H06_T0_BATCH02_FREEZE_NOTE.md'; np.write_text('\n'.join(note)+'\n',encoding='utf-8')
checks=OUT/'H06_T0_BATCH02_CHECKSUMS.txt'
with checks.open('w') as f:
    for p in [SCORES,filing_path,cp,np]: f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n")
status={'companies':len(company),'filings':len(filing),'high':high,'low':26-high,'acceleration_yes':acc,'acceleration_no':26-acc}
(OUT/'batch02_status.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status))
