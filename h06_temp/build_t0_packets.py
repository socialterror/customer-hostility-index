import csv,re,html,urllib.request,pathlib,time,json
from collections import defaultdict

ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'t0_packets'; OUT.mkdir(exist_ok=True)
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
UA='Customer Hostility Index academic research contact: jared.longhitano@gmail.com'

KEYS={
'SP001':['unauthorized','unlicensed','sharing','shared account','password sharing','entitlement','piracy','free user','non-paying','nonpaying','convert','conversion','monetize','monetization','access'],
'SP002':['price','pricing','rate','fee','fees','average revenue','arpu','upsell','cross-sell','premium','tier','package','packaging','bundle','subscription','yield','revenue per','lifetime value','spend per','attach rate','plan mix'],
'SP003':['legacy','sunset','retire','retirement','deprioritize','de-prioritize','migration','migrate','transition','phase out','phase-out','end of life','end-of-life','discontinue','discontinuation','withdraw','maintenance mode','consolidat'],
'SP004':['inflation','cost pressure','higher costs','increased costs','input cost','commodity','freight','labor cost','wage','tariff','surcharge','pass through','pass-through','recover costs','cost recovery','pricing actions','price increase','raise prices','increased pricing']}

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=90) as r:return r.read().decode('latin-1','replace')

def clean(txt):
    txt=re.sub(r'(?is)<script.*?</script>|<style.*?</style>',' ',txt)
    txt=re.sub(r'(?is)<[^>]+>',' ',txt)
    txt=html.unescape(txt).replace('\xa0',' ')
    txt=re.sub(r'[ \t\r\f\v]+',' ',txt)
    txt=re.sub(r'\n\s*\n+','\n',txt)
    return txt

def passages(txt):
    # split into sentence-ish lines, retain broad windows around any taxonomy keyword
    s=re.split(r'(?<=[.!?])\s+|\n+',txt)
    out=[]; seen=set()
    low=[x.lower() for x in s]
    for fam,ks in KEYS.items():
        hits=[]
        for i,x in enumerate(low):
            if any(k in x for k in ks):
                a=max(0,i-1); b=min(len(s),i+2)
                p=' '.join(s[a:b]).strip()
                if len(p)<80: continue
                key=re.sub(r'\s+',' ',p.lower())[:500]
                if key in seen: continue
                seen.add(key); hits.append(p[:1800])
        # cap but preserve spread through doc
        if len(hits)>36:
            idx=sorted(set(round(i*(len(hits)-1)/35) for i in range(36)))
            hits=[hits[i] for i in idx]
        out.append((fam,hits))
    return out

def main():
    rows=list(csv.DictReader(MAN.open()))
    by=defaultdict(list)
    for r in rows: by[int(r['sample_order'])].append(r)
    summary=[]
    for order in sorted(by):
        rs=sorted(by[order],key=lambda x:x['filing_position'])
        ticker=rs[0]['ticker']
        packet=[f'# H06 BLIND T0 EVIDENCE PACKET — {order:03d} {ticker}', '', 'Only frozen F1–F5 SEC filings. No post-F5 content.', '']
        for r in rs:
            raw=fetch(r['sec_locator']); txt=clean(raw); fams=passages(txt)
            packet += [f"## {r['filing_position']} | {r['form']} | {r['filing_date']} | {r['accession_number']}", '']
            total=0
            for fam,hits in fams:
                packet.append(f'### {fam}')
                if not hits: packet.append('- NO KEYWORD-CANDIDATE PASSAGE')
                for h in hits:
                    packet.append('- '+re.sub(r'\s+',' ',h))
                packet.append(''); total+=len(hits)
            summary.append({'sample_order':order,'ticker':ticker,'filing_position':r['filing_position'],'accession':r['accession_number'],'candidate_passages':total})
            time.sleep(.12)
        (OUT/f'{order:03d}_{ticker}.md').write_text('\n'.join(packet),encoding='utf-8')
    with (OUT/'packet_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=summary[0].keys());w.writeheader();w.writerows(summary)
    print(json.dumps({'packets':len(by),'filings':len(rows),'out':str(OUT)},indent=2))
if __name__=='__main__':main()
