import csv,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
src=ROOT/'t0_review'/'batch09_11_compact.tsv'; out=ROOT/'t0_review'/'final41_micro.md'
rows=list(csv.DictReader(src.open(encoding='utf-8'),delimiter='\t'))
def clean(s):
 s=re.sub(r'\s+',' ',s)
 return s[:380]
lines=['# H06 Final 41 Blind Micro Review','', 'Retrieval-only evidence compression; no automated classification.','']
for r in rows:
 lines += [f"## {int(r['order']):03d} {r['ticker']}", f"F1: {clean(r['F1_best'])}", f"F5: {clean(r['F5_best'])}", f"MID: {clean(r['mid_best'])}",'']
out.write_text('\n'.join(lines),encoding='utf-8')
print('micro',len(rows))
