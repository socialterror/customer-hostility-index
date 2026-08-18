import csv, pathlib, re, json, time, urllib.request, urllib.parse, html, datetime as dt
from collections import defaultdict

ROOT=pathlib.Path(__file__).resolve().parent
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
OUT=ROOT/'outcome_audit'; OUT.mkdir(exist_ok=True)
PACK=OUT/'candidate_packets'; PACK.mkdir(exist_ok=True)
UA={'User-Agent':'CHI-H06-outcome-audit research contact jlonghitano@gmail.com'}

TERMS=[
'price increase','prices increased','pricing action','pricing actions','raise prices','raised prices','rate increase','rate increases',
'fee increase','new fee','surcharge','fuel surcharge','inflation surcharge','pass through','pass-through','cost recovery','recover costs',
'premium tier','premium plan','paid add-on','add-on fee','subscription price','subscription fee','upgrade','upsell','monetize','monetization',
'discontinue','discontinued','retire','retired','sunset','phase out','migration','migrate','perpetual license','subscription model','sharing','shared account','seat'
]

rows=list(csv.DictReader(MAN.open(encoding='utf-8')))
companies=[]
for r in rows:
    if r['filing_position']=='F5':
        f5=dt.date.fromisoformat(r['filing_date'])
        try: end=f5.replace(year=f5.year+2)
        except ValueError: end=f5.replace(year=f5.year+2, day=28)
        companies.append({'sample_order':int(r['sample_order']),'ticker':r['ticker'],'company_name':r['company_name'],'CIK':r['CIK'],'F5_date':str(f5),'start':str(f5+dt.timedelta(days=1)),'end':str(end)})
companies.sort(key=lambda x:x['sample_order'])

# SEC master indices covering all possible outcome windows.
def get(url, timeout=30):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=timeout) as resp:
        return resp.read().decode('utf-8','ignore')

sec_by_cik=defaultdict(list)
for year in (2020,2021,2022):
  for q in (1,2,3,4):
    if year==2020 and q<4: continue
    url=f'https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{q}/master.idx'
    try: txt=get(url)
    except Exception as e:
        print('SEC IDX FAIL',year,q,e); continue
    for line in txt.splitlines():
        if '|' not in line: continue
        p=line.split('|')
        if len(p)!=5: continue
        cik,name,form,date,path=p
        if form not in ('10-Q','10-K','8-K'): continue
        sec_by_cik[cik.zfill(10)].append((date,form,path))
    time.sleep(0.12)

sent_split=re.compile(r'(?<=[.!?])\s+')
def extract_hits(text):
    text=html.unescape(re.sub(r'<[^>]+>',' ',text))
    text=re.sub(r'\s+',' ',text)
    sents=sent_split.split(text)
    out=[]
    for s in sents:
        lo=s.lower()
        mt=[t for t in TERMS if t in lo]
        if mt and 80<=len(s)<=1600:
            out.append((mt,s[:1600]))
    # de-dupe
    seen=set(); clean=[]
    for mt,s in out:
        k=re.sub(r'\W+',' ',s.lower())[:220]
        if k not in seen:
            seen.add(k); clean.append((mt,s))
    return clean[:120]

def gdelt_search(name,start,end):
    # broad contemporaneous news candidate search; results are candidate evidence only, never auto-classified.
    q=f'"{name}" ("price increase" OR "rate increase" OR surcharge OR "new fee" OR "subscription price" OR discontinue OR retired OR migration OR monetization OR premium)'
    params={
      'query':q,'mode':'ArtList','maxrecords':'75','format':'json','sort':'HybridRel',
      'startdatetime':start.replace('-','')+'000000','enddatetime':end.replace('-','')+'235959'
    }
    url='https://api.gdeltproject.org/api/v2/doc/doc?'+urllib.parse.urlencode(params)
    try:
        data=json.loads(get(url,45))
    except Exception as e:
        return [],str(e)
    arts=data.get('articles',[]) if isinstance(data,dict) else []
    keep=[]
    for a in arts[:75]:
        keep.append({k:a.get(k,'') for k in ('title','url','domain','seendate','language','sourcecountry')})
    return keep,''

summary=[]
for c in companies:
    order=c['sample_order']; cik=c['CIK'].zfill(10); start=c['start']; end=c['end']
    lines=[f"# H06 blinded outcome candidate packet — {order:03d} {c['ticker']}","",f"Company: {c['company_name']}",f"CIK: {cik}",f"F5: {c['F5_date']}",f"Outcome window: {start} through {end} inclusive","","NOTE: Retrieval-only packet. No predictor data read. No automated outcome classification.",""]
    sec_hits=0; sec_filings=0
    for date,form,path in sorted(sec_by_cik.get(cik,[])):
        if not (start<=date<=end): continue
        sec_filings+=1
        url='https://www.sec.gov/Archives/'+path
        try: text=get(url,45)
        except Exception as e:
            lines += [f"## SEC {date} {form}",f"FETCH_ERROR: {e}",""]; continue
        hits=extract_hits(text); sec_hits+=len(hits)
        lines += [f"## SEC {date} {form}",f"Source: {url}"]
        if hits:
            for mt,s in hits: lines.append(f"- TERMS[{'; '.join(mt)}] {s}")
        else: lines.append('- NO_TERM_HITS')
        lines.append('')
        time.sleep(0.08)
    arts,gerr=gdelt_search(c['company_name'],start,end)
    lines += ["## GDELT contemporaneous news candidates"]
    if gerr: lines.append('GDELT_ERROR: '+gerr)
    elif not arts: lines.append('- NO_CANDIDATES_RETURNED')
    else:
        for a in arts:
            lines.append(f"- {a['seendate']} | {a['domain']} | {a['title']} | {a['url']}")
    p=PACK/f"{order:03d}_{c['ticker']}.md"; p.write_text('\n'.join(lines),encoding='utf-8')
    summary.append({**c,'sec_filings_audited':sec_filings,'sec_candidate_passages':sec_hits,'news_candidates':len(arts),'gdelt_error':gerr})
    print(order,c['ticker'],sec_filings,sec_hits,len(arts),gerr[:60])
    time.sleep(0.18)

with (OUT/'candidate_summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
(OUT/'candidate_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('DONE',len(summary))
