import csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
src=ROOT/'t0_review'/'batch09_11_compact.tsv'; rows=list(csv.DictReader(src.open(encoding='utf-8'),delimiter='\t'))
for lo,hi,name in [(204,213,'realestate_tail'),(214,225,'utilities')]:
 lines=[]
 for r in rows:
  o=int(r['order'])
  if lo<=o<=hi:
   lines += [f'## {o:03d} {r["ticker"]}', 'F1 '+r['F1_best'][:650], 'F5 '+r['F5_best'][:650], 'MID '+r['mid_best'][:650], '']
 (ROOT/'t0_review'/f'{name}_review.md').write_text('\n'.join(lines),encoding='utf-8')
print('done',len(rows))
