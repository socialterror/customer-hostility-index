import csv,pathlib,hashlib,json
ROOT=pathlib.Path(__file__).resolve().parent
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'; SCORES=ROOT/'t0_scoring'/'batch03_company_scores.csv'; OUT=ROOT/'t0_scoring'
scores=list(csv.DictReader(SCORES.open(encoding='utf-8'))); by={int(r['sample_order']):r for r in scores}
manifest=[r for r in csv.DictReader(MAN.open(encoding='utf-8')) if 36<=int(r['sample_order'])<=51]
assert len(scores)==16 and len(manifest)==80
filing=[]
for m in manifest:
 s=by[int(m['sample_order'])]; p=m['filing_position']; cls=s[f'{p}_class']; strength=s[f'{p}_strength']
 filing.append({'sample_order':m['sample_order'],'sector':m['sector'],'ticker':m['ticker'],'company_name':m['company_name'],'CIK':m['CIK'],'filing_position':p,'form':m['form'],'filing_date':m['filing_date'],'accession_number':m['accession_number'],'sec_locator':m['sec_locator'],'classification':cls,'signal_strength':strength,'temporal_state':'N/A' if cls in ('No Signal','Neutral') else 'IMPLEMENTATION','affected_actor':s['affected_actor'] if cls not in ('No Signal','Neutral') else 'N/A','origin_status':'Company-originated commercial model' if cls not in ('No Signal','Neutral') else 'N/A','evidence_summary':s['trajectory_rationale'],'specificity':'High' if strength in ('Strong','Very Strong') else ('Moderate' if strength=='Moderate' else 'N/A'),'novelty':'Increasing' if s['semantic_acceleration']=='YES' and p=='F5' else ('Pre-existing' if cls not in ('No Signal','Neutral') else 'None'),'persistence':'Persistent' if cls not in ('No Signal','Neutral') else 'None','commercial_explicitness':'High' if strength in ('Strong','Very Strong') else ('Moderate' if strength=='Moderate' else 'N/A'),'scorer_confidence':s['scorer_confidence']})
fp=OUT/'H06_T0_SIGNAL_LEDGER_WORKING_BATCH03_CONSUMER_STAPLES.csv'
with fp.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=filing[0].keys());w.writeheader();w.writerows(filing)
fields=['sample_order','sector','ticker','company_name','F5_class','F5_strength','H06_intensity_binary','semantic_acceleration','affected_actor','trajectory_rationale','scorer_confidence']
cp=OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH03_FROZEN.csv'
with cp.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields+['batch_status']);w.writeheader();
 for s in scores:w.writerow({**{k:s[k] for k in fields},'batch_status':'FROZEN_WITHIN_BATCH_PRE_OUTCOME'})
high=sum(s['H06_intensity_binary']=='HIGH' for s in scores);acc=sum(s['semantic_acceleration']=='YES' for s in scores)
lines=['# H06 Blind T0 Scoring — Batch 03 Freeze Note','','**Sector:** Consumer Staples  ','**Companies:** 16  ','**Filings:** 80  ','**Status:** FROZEN WITHIN BATCH — PRE-OUTCOME','','No post-F5 outcome information was inspected or used.','','| # | Ticker | F5 class | F5 strength | Intensity | Acceleration |','|---:|---|---|---|---|---|']
for s in scores:lines.append(f"| {s['sample_order']} | {s['ticker']} | {s['F5_class']} | {s['F5_strength']} | {s['H06_intensity_binary']} | {s['semantic_acceleration']} |")
lines+=['','## Batch totals','',f'- High Signal Intensity: {high}',f'- Low Signal Intensity: {16-high}',f'- Semantic Acceleration YES: {acc}',f'- Semantic Acceleration NO: {16-acc}','','These calls are frozen before later sectors are scored.']
np=OUT/'H06_T0_BATCH03_FREEZE_NOTE.md';np.write_text('\n'.join(lines)+'\n',encoding='utf-8')
ck=OUT/'H06_T0_BATCH03_CHECKSUMS.txt'
with ck.open('w') as f:
 for p in [SCORES,fp,cp,np]:f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n")
status={'companies':16,'filings':80,'high':high,'low':16-high,'acceleration_yes':acc,'acceleration_no':16-acc}
(OUT/'batch03_status.json').write_text(json.dumps(status,indent=2)+'\n');print(status)
