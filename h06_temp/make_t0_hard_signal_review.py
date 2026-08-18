import pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_digests'; OUT=ROOT/'t0_review'; OUT.mkdir(exist_ok=True)
PHRASES=[
'price increase','pricing action','higher retail price','higher wholesale price','higher full-price','higher asp','average ticket','customer spend','wallet share','premium ticket','premiumization','premium product','increase prices','raise prices','pass along','pass through','pass-through','cost recovery','recover cost','surcharge','tariff','inflation','input cost','commodity price','freight cost','labor cost','wage increase','discontinue','discontinuation','sunset','phase out','migration','migrate','shift the primary','portfolio simplif','depriorit','retire','unauthorized use','unauthorized access to content','piracy','microtransaction','upsell','cross-sell','revenue per customer','revenue per subscriber','arpu','rate increase','higher rates','rate adjustments','lower discounts','full-price'
]
for order in range(10,36):
    files=list(SRC.glob(f'{order:03d}_*.md'))
    if not files: continue
    p=files[0]; ticker=p.stem.split('_',1)[1]
    lines=p.read_text(encoding='utf-8').splitlines()
    filing=''; fam=''; hits=[]
    for line in lines:
        if line.startswith('## '): filing=line.split('|')[0].replace('##','').strip()
        elif line.startswith('### '): fam=line[4:].strip()
        elif line.startswith('- ['):
            lo=line.lower()
            matched=[x for x in PHRASES if x in lo]
            if matched:
                score=float(re.match(r'- \[([0-9.]+)\]',line).group(1)); hits.append((filing,fam,score,','.join(matched),line.split('] ',1)[1]))
    hits=sorted(hits,key=lambda x:({'F1':0,'F5':1}.get(x[0],2),-x[2]))
    # keep max 3 per filing-family, but prioritize F1/F5
    kept=[]; counts={}
    for h in hits:
        key=(h[0],h[1]);
        if counts.get(key,0)>=3: continue
        kept.append(h); counts[key]=counts.get(key,0)+1
    text=[f'# {order:03d} {ticker} hard-signal review','', 'Retrieval-only; explicit mechanism phrase matches. No automated classification.','']
    for h in kept:
        text.append(f'- **{h[0]} {h[1]} [{h[2]:.1f}] ({h[3]})** — {h[4]}')
    (OUT/f'{order:03d}_{ticker}_hard.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
# combined
parts=[]
for p in sorted(OUT.glob('0??_*_hard.md')): parts.append(p.read_text(encoding='utf-8'))
(OUT/'batch02_hard_signal_review.md').write_text('\n'.join(parts),encoding='utf-8')
print(len(parts))
