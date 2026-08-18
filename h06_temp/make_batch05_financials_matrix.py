import pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_review'; OUT=ROOT/'t0_review'/'batch05_financials_matrix.md'
ORD=range(63,99)
STRONG=[
('fee increase',12),('increase fees',12),('higher fees',10),('service charge',10),('account fee',10),('transaction fee',10),('interchange',9),('commission',8),('pricing action',10),('price increase',10),('higher pricing',9),('advisory fee',10),('management fee',9),('premium',6),('waive',7),('waiver',7),('subscription',8),('tier',7),('pricing',4),('fees',4),('fee',3),('client',2),('customer',2),('cardholder',3),('merchant',3)]
NOISE=['interest rate swap','fair value','weighted average','discount rate','tax rate','exchange rate','derivative','pension','share repurchase','average price paid per share','securities pricing']
def score(line):
 t=line.lower(); s=0
 for k,w in STRONG:
  if k in t:s+=w
 if any(x in t for x in ['customer','client','merchant','cardholder','account holder','policyholder','subscriber']):s+=4
 if any(x in t for x in NOISE):s-=8
 if 'interest rate' in t and not any(x in t for x in ['customer','loan','deposit','card']):s-=6
 return s
out=['# H06 Batch05 Financials customer-mechanism matrix','','Retrieval-only ranking from exact frozen F1–F5 hard reviews. No automated classification.','']
for o in ORD:
 files=list(SRC.glob(f'{o:03d}_*_hard.md'))
 if not files: continue
 p=files[0]; lines=p.read_text(encoding='utf-8').splitlines(); cand=[]
 for ln in lines:
  if not ln.startswith('- **'): continue
  sc=score(ln)
  if sc>=6:cand.append((sc,ln))
 # preserve F1/F5 visibility, then strongest remaining
 picks=[]
 for label in ['F1','F5']:
  vals=sorted([x for x in cand if f'**{label} ' in x[1]],key=lambda x:-x[0])[:5]
  picks+=vals
 rest=sorted([x for x in cand if x not in picks],key=lambda x:-x[0])[:8]
 picks+=rest
 out += [f'## {p.stem.replace("_hard","")}', '']
 if not picks: out.append('- NO CUSTOMER-FACING FEE/PRICING CANDIDATE ABOVE FILTER')
 else:
  for sc,ln in picks: out.append(f'- [{sc}] '+ln[2:])
 out.append('')
OUT.write_text('\n'.join(out)+'\n',encoding='utf-8')
print(OUT)