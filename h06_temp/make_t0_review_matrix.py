import pathlib,re,csv
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_digests'; OUT=ROOT/'t0_review'; OUT.mkdir(exist_ok=True)
MIN_ORDER=10; MAX_ORDER=35
rows=[]
for path in sorted(SRC.glob('[0-9][0-9][0-9]_*.md')):
    order=int(path.name[:3])
    if not (MIN_ORDER<=order<=MAX_ORDER): continue
    ticker=path.stem.split('_',1)[1]
    filing=None; fam=None
    bucket={}
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            filing=line.split('|')[0].replace('##','').strip()
        elif line.startswith('### '): fam=line[4:].strip()
        elif line.startswith('- [') and filing and fam:
            m=re.match(r'- \[([0-9.]+)\] (.*)',line)
            if m:
                score=float(m.group(1)); text=m.group(2)
                bucket.setdefault((filing,fam),[]).append((score,text))
    for fam in ['SP001','SP002','SP003','SP004']:
        for filing in ['F1','F5']:
            vals=sorted(bucket.get((filing,fam),[]), reverse=True)
            if vals: rows.append([order,ticker,filing,fam,vals[0][0],vals[0][1]])
        mids=[]
        for filing in ['F2','F3','F4']:
            mids += [(s,t,filing) for s,t in bucket.get((filing,fam),[])]
        if mids:
            s,t,filing=max(mids,key=lambda x:x[0]); rows.append([order,ticker,'MID-'+filing,fam,s,t])
with (OUT/'batch02_review_matrix.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['sample_order','ticker','position','family','retrieval_score','passage']); w.writerows(rows)
# markdown grouped
lines=['# H06 Batch 02 Blind Review Matrix','','Retrieval-only. No automated semantic classification.','']
for order in range(MIN_ORDER,MAX_ORDER+1):
    rr=[r for r in rows if r[0]==order]
    if not rr: continue
    lines += [f"## {order:03d} {rr[0][1]}",'']
    for r in rr:
        lines.append(f"- **{r[2]} {r[3]} [{r[4]:.1f}]** — {r[5]}")
    lines.append('')
(OUT/'batch02_review_matrix.md').write_text('\n'.join(lines),encoding='utf-8')
print(len(rows))
