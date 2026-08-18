import pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_review'; OUT=ROOT/'t0_review'/'batch05_financials_compact.tsv'
POS=['fee increase','increase fees','higher fees','service charge','account fee','transaction fee','interchange','commission','pricing action','price increase','higher pricing','premium rate increase','rate increase','re-price','repric','cross-sell','advisory fee','management fee','subscription','tier','pricing','fees','fee','premium','spread']
ACT=['customer','client','merchant','cardholder','policyholder','account','consumer','participant']
NOISE=['interest rate swap','fair value','weighted average','discount rate','tax rate','exchange rate','derivative','pension','share repurchase','average price paid per share']
def score(s):
 t=s.lower(); sc=sum(4 for k in POS if k in t)+sum(2 for k in ACT if k in t)-sum(5 for k in NOISE if k in t)
 return sc
def clean(s):
 s=re.sub(r'^- \*\*','',s); s=re.sub(r'\*\* — ',' | ',s); s=re.sub(r'\s+',' ',s).strip(); return s[:420]
rows=['order\tticker\tF1_best\tF5_best\tmid_best']
for o in range(63,99):
 fs=list(SRC.glob(f'{o:03d}_*_hard.md'))
 if not fs: continue
 p=fs[0]; ticker=p.stem.split('_')[1]; lines=[x for x in p.read_text(encoding='utf-8').splitlines() if x.startswith('- **')]
 def best(label):
  a=[(score(x),x) for x in lines if f'**{label} ' in x]
  a.sort(key=lambda z:-z[0]); return clean(a[0][1]) if a and a[0][0]>=2 else 'NONE'
 mid=[]
 for x in lines:
  if any(f'**F{i} ' in x for i in [2,3,4]): mid.append((score(x),x))
 mid.sort(key=lambda z:-z[0]); mb=clean(mid[0][1]) if mid and mid[0][0]>=2 else 'NONE'
 rows.append(f'{o}\t{ticker}\t{best("F1")}\t{best("F5")}\t{mb}')
OUT.write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(len(rows)-1)