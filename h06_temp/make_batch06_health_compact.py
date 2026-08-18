import pathlib,re,csv
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_packets'; OUT=ROOT/'t0_review'; OUT.mkdir(exist_ok=True)
MIN_ORDER=99; MAX_ORDER=126
PHRASES=['price increase','pricing action','pricing actions','higher price','higher prices','higher asp','average selling price','average price','rate increase','rate increases','premium increase','premium increases','reimbursement','rebate','discount','list price','net price','price reduction','price erosion','pass through','pass-through','cost recovery','recover cost','surcharge','tariff','inflation','input cost','raw material','freight cost','labor cost','wage','discontinue','discontinuation','sunset','phase out','migration','migrate','portfolio','depriorit','retire','unauthorized use','unauthorized access to content','piracy','upsell','cross-sell','revenue per customer','revenue per member','premiumization']
rows=[]
for order in range(MIN_ORDER,MAX_ORDER+1):
    files=list(SRC.glob(f'{order:03d}_*.md'))
    if not files: continue
    p=files[0]; ticker=p.stem.split('_',1)[1]
    filing=''; fam=''; hits=[]
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '): filing=line.split('|')[0].replace('##','').strip()
        elif line.startswith('### '): fam=line[4:].strip()
        elif line.startswith('- ') and filing and fam:
            lo=line.lower(); matched=[x for x in PHRASES if x in lo]
            if matched:
                score=sum(1 for x in matched if x in lo)
                for x in ['price increase','pricing action','higher price','rate increase','list price','net price','pass through','pass-through','cost recovery','surcharge','discontinue','migration','migrate','premiumization']:
                    if x in lo: score += 3
                hits.append((filing,fam,score,','.join(matched),line[2:]))
    def best(pos):
        cand=[h for h in hits if h[0]==pos]
        return max(cand,key=lambda x:x[2]) if cand else None
    f1=best('F1'); f5=best('F5')
    mids=[h for h in hits if h[0] in ('F2','F3','F4')]; mid=max(mids,key=lambda x:x[2]) if mids else None
    def fmt(h):
        if not h: return 'NONE'
        return f'{h[0]} {h[1]} [{h[2]}] ({h[3]}) | {h[4][:900]}'
    rows.append([order,ticker,fmt(f1),fmt(f5),fmt(mid)])
with (OUT/'batch06_health_care_compact.tsv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f,delimiter='\t'); w.writerow(['order','ticker','F1_best','F5_best','mid_best']); w.writerows(rows)
print(len(rows))
# retrigger after workflow registration
