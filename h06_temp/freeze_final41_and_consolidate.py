import csv,json,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'t0_scoring'; OUT.mkdir(exist_ok=True)
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
# Blind T0 adjudications only. No post-F5 outcome information used.
D={
185:('NUE','SP004','Moderate','LOW','NO','Steel customers','A raw-material surcharge/variable pricing mechanism is described, but it is conditional and not Strong at F5.'),
186:('PKG','SP002','Strong','HIGH','NO','Containerboard/box customers','F5 explicitly announces containerboard and box price increases; pricing was already an operating mechanism at F1, so no acceleration.'),
187:('ALB','SP004','Moderate','LOW','NO','Chemical/materials customers','Ability to pass raw-material and energy cost increases is explicit but risk-framed rather than a Strong implemented F5 transfer.'),
188:('CF','No Signal','N/A','LOW','NO','N/A','Selling prices are commodity/market outcomes rather than a company-originated customer-economic mechanism.'),
189:('MLM','SP002','Moderate','LOW','NO','Aggregates customers','Average selling-price gains are present but the frozen trajectory does not establish a Strong company-originated yield mechanism at F5.'),
190:('BLL','SP004','Very Strong','HIGH','NO','Packaging customers','Contracts covering the majority of volume explicitly pass aluminum/metal price changes through to customers from F1 through F5; very strong but static.'),
191:('MOS','No Signal','N/A','LOW','NO','N/A','Fertilizer selling-price movements are described as market-price dynamics rather than a new company-originated customer action.'),
192:('SEE','No Signal','N/A','LOW','NO','N/A','Discontinued-operation and reference-rate accounting language is non-qualifying.'),
193:('SHW','No Signal','N/A','LOW','NO','N/A','Earlier selling-price increases are not carried into F5 as a qualifying Strong customer mechanism; F5 is dominated by mix and moderating raw-material costs.'),
194:('CE','No Signal','N/A','LOW','NO','N/A','Pass-through/price-increase language remains generic risk framing and is not a qualifying F5 action.'),
195:('IFF','SP004','Moderate','LOW','NO','Scent/flavor customers','Earlier price increases offset input costs, but F5 does not retain a Strong current transfer mechanism.'),
196:('IP','SP002','Moderate','LOW','NO','Pulp/containerboard customers','F5 projects higher price realization based on current pricing, but the evidence remains below Strong and does not establish acceleration.'),
197:('WRK','No Signal','N/A','LOW','NO','N/A','Discontinued-operation, financing-rate and selling-price/mix references do not establish a qualifying F5 mechanism.'),
198:('EQIX','No Signal','N/A','LOW','NO','N/A','Utility price increases are Equinix input costs, not a customer transfer mechanism.'),
199:('SBAC','SP004','Strong','HIGH','NO','Tower tenants','Tenant/site leases explicitly contain rent escalators and pass-through charges for underlying ground rent; established contractual transfer, no acceleration.'),
200:('AMT','SP004','Very Strong','HIGH','NO','Tower tenants','Most tenant leases periodically increase rent and some explicitly pass through ground-rent, power and fuel costs; very strong and present from F1.'),
201:('PEAK','SP002','Moderate','LOW','NO','Healthcare-property tenants','Annual/rental-rate increases contribute to cash flow, but F5 evidence is not Strong enough for High intensity.'),
202:('CBRE','No Signal','N/A','LOW','NO','N/A','Inflation and interest-rate references concern market conditions/costs rather than customer-economic action.'),
203:('PSA','SP002','Very Strong','HIGH','NO','Self-storage tenants','F5 explicitly resumes rate increases to existing long-term tenants and raises new-tenant rental rates; mechanism is established/resumed rather than new.'),
204:('ESS','SP002','Moderate','LOW','NO','Apartment residents','Rental-rate economics are explicit, but F5 does not show a Strong yield action after the temporary no-increase period.'),
205:('HST','No Signal','N/A','LOW','NO','N/A','Travel/migration and financing-rate language is non-qualifying.'),
206:('VNO','SP004','Moderate','LOW','NO','Commercial tenants','Leases contain rent step-ups and operating-cost/utility pass-throughs, but F5 does not present a Strong current mechanism.'),
207:('VTR','No Signal','N/A','LOW','NO','N/A','F1 contractual rent escalation is not sustained as a qualifying Strong F5 signal.'),
208:('AIV','SP002','Moderate','LOW','NO','Apartment residents','Renewal/new-lease rent growth is an established mechanism, but F5 evidence is below Strong.'),
209:('DRE','SP002','Moderate','LOW','NO','Industrial tenants','Rental-rate growth/re-leasing contributes to revenue, but no Strong new F5 yield mechanism is identified.'),
210:('WELL','SP002','Strong','HIGH','NO','Triple-net tenants','F5 explicitly reports contractual rental-rate increases under escalators; strong but already present at F1.'),
211:('AVB','SP002','Moderate','LOW','NO','Apartment residents','Rental-rate economics persist, but F5 is dominated by regulatory constraints/hypothetical caps rather than a Strong company action.'),
212:('DLR','SP002','Moderate','LOW','NO','Data-center tenants','Rental rates and renewals are central to the lease model, but F5 evidence does not reach Strong.'),
213:('REG','SP002','Moderate','LOW','NO','Retail-center tenants','Rental-rate growth on new/renewal leases is established but F5 evidence remains below Strong.'),
214:('LNT','SP004','Very Strong','HIGH','NO','Regulated utility customers','Approved base-rate increases, riders and cost-recovery mechanisms are explicit from F1 through F5; very strong but static.'),
215:('ED','SP002','Strong','HIGH','NO','Regulated utility customers','Multi-year approved base-rate plans are already explicit early in the trajectory and remain operative; strong but non-accelerating.'),
216:('CNP','No Signal','N/A','LOW','NO','N/A','The prominent frozen-window mechanisms return tax benefits/credits to customers or discuss pending recovery; no qualifying High F5 customer extraction signal.'),
217:('D','SP004','Very Strong','HIGH','NO','Regulated utility customers','Riders and purchased-gas/base-rate recovery explicitly transfer approved costs into customer rates from the opening filings; very strong but static.'),
218:('CMS','SP002','Very Strong','HIGH','YES','Regulated utility customers','Trajectory strengthens from customer refunds/rate-risk framing to an approved $144 million annual rate increase effective October 1, 2020; material concrete implementation.'),
219:('DTE','SP002','Strong','HIGH','YES','Regulated utility customers','Trajectory moves from generic regulatory/cost-recovery exposure to explicit large base-rate requests tied to infrastructure and O&M investment; materially more concrete.'),
220:('PNW','SP002','Very Strong','HIGH','NO','Regulated utility customers','A specific $69 million retail base-rate increase application is already explicit at F1 and remains the same mechanism through F5.'),
221:('FE','SP004','Very Strong','HIGH','NO','Regulated utility customers','Distribution riders and quarterly cost recovery are explicit from F1; later cap/rate approvals strengthen magnitude but do not introduce a new mechanism.'),
222:('DUK','SP002','Very Strong','HIGH','NO','Regulated utility customers','A 12.3% retail base-revenue increase request is already explicit at F1; subsequent settlement/recovery proceedings are continuation, not acceleration.'),
223:('EVRG','SP004','Moderate','LOW','NO','Regulated utility customers','Cost-recovery architecture is explicit, but rate moratoria and under-recovery risk keep F5 below Strong customer-transfer intensity.'),
224:('EIX','SP004','Moderate','LOW','NO','Regulated utility customers','Customer price/cost recovery is discussed through balancing accounts, but F5 does not establish a Strong new company-originated transfer mechanism.'),
225:('AES','SP004','Moderate','LOW','NO','Regulated utility customers','Cost-recovery mechanisms exist, while F5 also describes constraints preventing contractual pass-through; intensity remains below Strong.')}
rows=list(csv.DictReader(MAN.open()))
# sector batches
ranges=[(9,'materials',185,197),(10,'real_estate',198,213),(11,'utilities',214,225)]
for batch,sector,lo,hi in ranges:
 company=[]; filings=[]
 for order in range(lo,hi+1):
  ticker,cls,strength,intensity,accel,actor,rat=D[order]
  rr=[r for r in rows if int(r['sample_order'])==order]; assert len(rr)==5 and rr[0]['ticker']==ticker
  name=rr[0]['company_name']
  company.append({'sample_order':order,'sector':sector,'ticker':ticker,'company_name':name,'F5_class':cls,'F5_strength':strength,'H06_intensity_binary':intensity,'semantic_acceleration':accel,'affected_actor':actor,'trajectory_rationale':rat,'batch_status':'FROZEN_WITHIN_BATCH_PRE_OUTCOME'})
  for r in rr:
   filings.append({**r,'classification':cls,'signal_strength':strength,'temporal_state':'IMPLEMENTATION' if cls not in ('No Signal','Neutral') else 'N/A','affected_actor':actor,'origin_status':'Company-originated commercial model' if cls not in ('No Signal','Neutral') else 'N/A','evidence_summary':rat})
 cp=OUT/f'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH{batch:02d}_FROZEN.csv'; fp=OUT/f'H06_T0_SIGNAL_LEDGER_WORKING_BATCH{batch:02d}_{sector.upper()}.csv'
 for p,data in [(cp,company),(fp,filings)]:
  with p.open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
 h=sum(x['H06_intensity_binary']=='HIGH' for x in company); ay=sum(x['semantic_acceleration']=='YES' for x in company)
 status={'companies':len(company),'filings':len(filings),'high':h,'low':len(company)-h,'acceleration_yes':ay,'acceleration_no':len(company)-ay}
 (OUT/f'batch{batch:02d}_status.json').write_text(json.dumps(status,indent=2)+'\n')
 note=OUT/f'H06_T0_BATCH{batch:02d}_FREEZE_NOTE.md'; note.write_text(f'# H06 Blind T0 Scoring — Batch {batch:02d} Freeze Note\n\nSector: {sector}\nCompanies: {len(company)}\nFilings: {len(filings)}\nHigh: {h}\nLow: {len(company)-h}\nAcceleration YES: {ay}\nAcceleration NO: {len(company)-ay}\n\nNo post-F5 outcome information was inspected or used.\n')
 with (OUT/f'H06_T0_BATCH{batch:02d}_CHECKSUMS.txt').open('w') as f:
  for p in (cp,fp,note): f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
# consolidate all frozen batch company ledgers + all signal ledgers
cfiles=sorted(OUT.glob('H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH*_FROZEN.csv'))
assert len(cfiles)==11, [p.name for p in cfiles]
allc=[]
for p in cfiles: allc.extend(csv.DictReader(p.open(encoding='utf-8')))
allc=sorted(allc,key=lambda r:int(r['sample_order']))
assert len(allc)==225 and [int(r['sample_order']) for r in allc]==list(range(1,226))
ffiles=sorted(OUT.glob('H06_T0_SIGNAL_LEDGER_WORKING_BATCH*.csv'))
assert len(ffiles)==11, [p.name for p in ffiles]
allf=[]
for p in ffiles: allf.extend(csv.DictReader(p.open(encoding='utf-8')))
allf=sorted(allf,key=lambda r:(int(r['sample_order']),r['filing_position']))
assert len(allf)==1125
assert len({(r['sample_order'],r['accession_number']) for r in allf})==1125
CP=OUT/'H06_COMPANY_PREDICTOR_LEDGER_FROZEN.csv'; FP=OUT/'H06_T0_SIGNAL_LEDGER_FROZEN.csv'
for p,data in [(CP,allc),(FP,allf)]:
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
h=sum(r['H06_intensity_binary']=='HIGH' for r in allc); ay=sum(r['semantic_acceleration']=='YES' for r in allc)
summary={'companies':225,'filings':1125,'high':h,'low':225-h,'acceleration_yes':ay,'acceleration_no':225-ay,'outcome_research':'CLOSED_NOT_USED','t0_status':'FROZEN'}
(OUT/'H06_T0_FINAL_FREEZE_STATUS.json').write_text(json.dumps(summary,indent=2)+'\n')
NOTE=OUT/'H06_T0_FINAL_FREEZE_NOTE.md'; NOTE.write_text(f'''# H06 Final Blind T0 Freeze\n\n**Status:** FROZEN — predictor construction complete; outcome audit may begin only after this freeze.\n\n- Companies: 225\n- Exact frozen filings: 1,125\n- High Signal Intensity: {h}\n- Low Signal Intensity: {225-h}\n- Semantic Acceleration YES: {ay}\n- Semantic Acceleration NO: {225-ay}\n- Post-F5 outcomes used during scoring: **NONE**\n\nThe company predictor ledger and filing-level T0 signal ledger are immutable inputs to the subsequent H06 outcome audit.\n''')
CH=OUT/'H06_T0_FINAL_CHECKSUMS.txt'
with CH.open('w') as f:
 for p in (CP,FP,NOTE,OUT/'H06_T0_FINAL_FREEZE_STATUS.json'):
  f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
print(summary)
print(CP,FP,NOTE,CH,sep='\n')
