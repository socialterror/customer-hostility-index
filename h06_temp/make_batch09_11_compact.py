import pathlib,re,csv
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_packets'; OUT=ROOT/'t0_review'; OUT.mkdir(exist_ok=True)
PHRASES=['price increase','pricing action','pricing actions','higher price','higher prices','price realization','price/mix','price mix','rate increase','rate increases','base rate','rate case','rates approved','rate adjustment','rider','surcharge','fuel surcharge','pass through','pass-through','cost recovery','recover costs','recovery of costs','purchased gas','fuel clause','tariff','raw material','freight cost','input cost','inflation','rent increase','rental rate','rental rates','rent growth','lease renewal','renewal rate','renewal rates','re-leasing','releasing spread','leasing spread','same-store rent','same store rent','rent per unit','tenant','premiumization','discontinue','discontinuation','sunset','phase out','migration','migrate','portfolio']
rows=[]
for order in range(185,226):
 fs=list(SRC.glob(f'{order:03d}_*.md'))
 if not fs: continue
 p=fs[0]; ticker=p.stem.split('_',1)[1]; filing=''; fam=''; hits=[]
 for line in p.read_text(encoding='utf-8').splitlines():
  if line.startswith('## '): filing=line.split('|')[0].replace('##','').strip()
  elif line.startswith('### '): fam=line[4:].strip()
  elif line.startswith('- ') and filing and fam:
   lo=line.lower(); matched=[x for x in PHRASES if x in lo]
   if matched:
    score=len(matched)
    for x in ['price increase','pricing action','higher price','price realization','rate increase','base rate','rate case','rider','surcharge','pass through','pass-through','cost recovery','recover costs','purchased gas','fuel clause','rent increase','rental rate','rent growth','lease renewal','re-leasing','same-store rent','same store rent','discontinue','migration','migrate']:
     if x in lo: score+=3
    hits.append((filing,fam,score,','.join(matched),line[2:]))
 def best(pos):
  c=[h for h in hits if h[0]==pos]; return max(c,key=lambda x:x[2]) if c else None
 f1=best('F1'); f5=best('F5'); mids=[h for h in hits if h[0] in ('F2','F3','F4')]; mid=max(mids,key=lambda x:x[2]) if mids else None
 def fmt(h): return 'NONE' if not h else f'{h[0]} {h[1]} [{h[2]}] ({h[3]}) | {h[4][:1000]}'
 rows.append([order,ticker,fmt(f1),fmt(f5),fmt(mid)])
with (OUT/'batch09_11_compact.tsv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f,delimiter='\t'); w.writerow(['order','ticker','F1_best','F5_best','mid_best']); w.writerows(rows)
sdir=OUT/'batch09_11_split'; sdir.mkdir(exist_ok=True)
for r in rows:
 (sdir/f'{r[0]:03d}_{r[1]}.md').write_text(f'# {r[0]:03d} {r[1]}\n\n## F1\n{r[2]}\n\n## F5\n{r[3]}\n\n## MID\n{r[4]}\n',encoding='utf-8')
print('final-sectors',len(rows))
# trigger
