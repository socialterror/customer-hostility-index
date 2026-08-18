import pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_packets'; OUT=ROOT/'t0_review'; OUT.mkdir(exist_ok=True)
PHRASES=[
'price increase','pricing action','pricing actions','higher prices','raise prices','increased prices','higher pricing','list price','net price','pricing realization','price/mix','price mix','revenue management','premiumization','premium product','premium mix','lower discounts','full-price','average selling price','average price','pass along','pass through','pass-through','cost recovery','recover cost','surcharge','inflation','input cost','commodity','freight','labor cost','wage','tariff','discontinue','discontinuation','sunset','phase out','migration','migrate','portfolio simplif','depriorit','retire','unauthorized','piracy','microtransaction','upsell','cross-sell','revenue per customer','revenue per subscriber','arpu','rate increase','higher rates','rate adjustments']
for order in range(36,52):
    files=list(SRC.glob(f'{order:03d}_*.md'))
    if not files: continue
    p=files[0]; ticker=p.stem.split('_',1)[1]
    filing=''; fam=''; hits=[]
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '): filing=line.split('|')[0].replace('##','').strip()
        elif line.startswith('### '): fam=line[4:].strip()
        elif line.startswith('- '):
            lo=line.lower(); matched=[x for x in PHRASES if x in lo]
            if matched:
                score=sum(3 if x in ('price increase','pricing action','pricing actions','pass along','pass through','pass-through','cost recovery','portfolio simplif','depriorit','sunset','phase out','unauthorized','piracy') else 1 for x in matched)
                hits.append((filing,fam,score,','.join(matched),line[2:]))
    hits=sorted(hits,key=lambda x:(0 if x[0]=='F1' else 1 if x[0]=='F5' else 2,-x[2]))
    kept=[]; counts={}
    for h in hits:
        key=(h[0],h[1])
        if counts.get(key,0)>=4: continue
        kept.append(h); counts[key]=counts.get(key,0)+1
    text=[f'# {order:03d} {ticker} hard-signal review','', 'Retrieval-only from exact frozen packets; no automated classification.','']
    for h in kept: text.append(f'- **{h[0]} {h[1]} [{h[2]}] ({h[3]})** — {h[4]}')
    (OUT/f'{order:03d}_{ticker}_hard.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
print('built',sum(1 for _ in range(36,52)))
