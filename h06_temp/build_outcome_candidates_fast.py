import csv, pathlib, re, json, time, urllib.request, urllib.parse, html, datetime as dt, os
from collections import defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
LO=int(os.environ.get('MIN_ORDER','1')); HI=int(os.environ.get('MAX_ORDER','225'))
OUT=ROOT/'outcome_audit_fast'; OUT.mkdir(exist_ok=True)
PACK=OUT/'candidate_packets'; PACK.mkdir(exist_ok=True)
UA={'User-Agent':'CHI-H06-outcome-audit research contact jlonghitano@gmail.com'}
TERMS=['price increase','prices increased','pricing action','pricing actions','raise prices','raised prices','rate increase','rate increases','fee increase','new fee','surcharge','fuel surcharge','inflation surcharge','pass through','pass-through','cost recovery','recover costs','premium tier','premium plan','paid add-on','add-on fee','subscription price','subscription fee','upgrade','upsell','monetize','monetization','discontinue','discontinued','retire','retired','sunset','phase out','migration','migrate','perpetual license','subscription model','shared account','sharing','seat']
rows=list(csv.DictReader(MAN.open(encoding='utf-8')))
companies=[]
for r in rows:
 if r['filing_position']=='F5' and LO<=int(r['sample_order'])<=HI:
  f5=dt.date.fromisoformat(r['filing_date'])
  try:end=f5.replace(year=f5.year+2)
  except ValueError:end=f5.replace(year=f5.year+2,day=28)
  companies.append({'sample_order':int(r['sample_order']),'ticker':r['ticker'],'company_name':r['company_name'],'CIK':r['CIK'],'F5_date':str(f5),'start':str(f5+dt.timedelta(days=1)),'end':str(end)})
companies.sort(key=lambda x:x['sample_order'])
def get(url,timeout=12):
 req=urllib.request.Request(url,headers=UA)
 with urllib.request.urlopen(req,timeout=timeout) as resp:return resp.read().decode('utf-8','ignore')
sec=defaultdict(list)
for year in (2020,2021,2022):
 for q in (1,2,3,4):
  if year==2020 and q<4:continue
  try:txt=get(f'https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{q}/master.idx')
  except Exception as e:print('IDX_FAIL',year,q,e);continue
  for line in txt.splitlines():
   if '|' not in line:continue
   p=line.split('|')
   if len(p)!=5:continue
   cik,name,form,date,path=p
   if form in ('10-Q','10-K'):sec[cik.zfill(10)].append((date,form,path))
split=re.compile(r'(?<=[.!?])\s+')
def hits(text):
 text=html.unescape(re.sub(r'<[^>]+>',' ',text));text=re.sub(r'\s+',' ',text)
 out=[];seen=set()
 for s in split.split(text):
  lo=s.lower();m=[t for t in TERMS if t in lo]
  if m and 80<=len(s)<=1800:
   k=re.sub(r'\W+',' ',s.lower())[:220]
   if k not in seen:seen.add(k);out.append((m,s[:1800]))
 return out[:100]
def gdelt(name,start,end):
 q=f'"{name}" ("price increase" OR "rate increase" OR surcharge OR "new fee" OR "subscription price" OR discontinue OR retired OR migration OR monetization OR premium)'
 params={'query':q,'mode':'ArtList','maxrecords':'50','format':'json','sort':'HybridRel','startdatetime':start.replace('-','')+'000000','enddatetime':end.replace('-','')+'235959'}
 try:data=json.loads(get('https://api.gdeltproject.org/api/v2/doc/doc?'+urllib.parse.urlencode(params),8))
 except Exception as e:return [],str(e)
 arts=data.get('articles',[]) if isinstance(data,dict) else []
 return [{k:a.get(k,'') for k in ('title','url','domain','seendate')} for a in arts[:50]],''
summary=[]
for c in companies:
 lines=[f"# H06 blinded outcome candidate packet — {c['sample_order']:03d} {c['ticker']}",'',f"Company: {c['company_name']}",f"CIK: {c['CIK'].zfill(10)}",f"F5: {c['F5_date']}",f"Outcome window: {c['start']} through {c['end']} inclusive",'', 'Retrieval-only. No predictor data read. No automated classification.','']
 sf=sh=0
 for date,form,path in sorted(sec.get(c['CIK'].zfill(10),[])):
  if not(c['start']<=date<=c['end']):continue
  sf+=1;url='https://www.sec.gov/Archives/'+path
  try:hs=hits(get(url,12))
  except Exception as e:lines += [f'## SEC {date} {form}',f'FETCH_ERROR: {e}',''];continue
  sh+=len(hs);lines += [f'## SEC {date} {form}',f'Source: {url}']
  lines += [f"- TERMS[{'; '.join(m)}] {s}" for m,s in hs] or ['- NO_TERM_HITS']; lines.append('')
 arts,err=gdelt(c['company_name'],c['start'],c['end']);lines += ['## GDELT contemporaneous news candidates']
 if err:lines.append('GDELT_ERROR: '+err)
 elif not arts:lines.append('- NO_CANDIDATES_RETURNED')
 else:
  for a in arts:lines.append(f"- {a['seendate']} | {a['domain']} | {a['title']} | {a['url']}")
 (PACK/f"{c['sample_order']:03d}_{c['ticker']}.md").write_text('\n'.join(lines),encoding='utf-8')
 summary.append({**c,'sec_filings_audited':sf,'sec_candidate_passages':sh,'news_candidates':len(arts),'gdelt_error':err})
 print(c['sample_order'],c['ticker'],sf,sh,len(arts),err[:30],flush=True)
with (OUT/f'candidate_summary_{LO:03d}_{HI:03d}.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=summary[0].keys());w.writeheader();w.writerows(summary)
print('DONE',LO,HI,len(summary))
