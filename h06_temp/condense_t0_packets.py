# trigger batch02 condensation 2026-08-18
import pathlib,re,json
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'t0_packets'; OUT=ROOT/'t0_digests'; OUT.mkdir(exist_ok=True)
WEIGHTS={
'SP001': [('password sharing',10),('shared account',10),('unauthorized',8),('unlicensed',8),('piracy',7),('non-paying',8),('nonpaying',8),('entitlement',7),('monetiz',5),('convert',4),('access',1)],
'SP002': [('higher average rates',10),('contractual rate increase',10),('price increase',10),('increased pricing',9),('pricing action',9),('rate increase',8),('average revenue per',8),('arpu',8),('premium',5),('tier',4),('bundle',4),('packag',4),('fee revenue',6),('higher fees',8),('pricing',3),('price',2),('subscription',3)],
'SP003': [('phase out',10),('sunset',10),('retire',9),('discontinu',9),('depriorit',9),('end of life',9),('migration',7),('migrate',7),('transition',5),('legacy',6),('consolidat',3),('withdraw',8)],
'SP004': [('pass-through',10),('pass through',10),('recover costs',10),('cost recovery',10),('surcharge',9),('input cost',8),('inflation',8),('higher costs',6),('increased costs',6),('commodity',5),('freight',5),('labor cost',5),('wage',4),('tariff',6),('pricing action',5),('price increase',5)]}
def score(text,fam):
    t=text.lower(); s=0
    for k,w in WEIGHTS[fam]:
        if k in t: s += w*(1+min(t.count(k)-1,2)*0.25)
    if any(x in t for x in ['customer','subscriber','affiliate','consumer','client','ratepayer']): s+=2
    if any(x in t for x in ['revenue','fee','rate','pricing','price']): s+=2
    return s
def parse(path):
    txt=path.read_text(encoding='utf-8'); lines=txt.splitlines(); head=lines[0]
    out=[head,'','Ranked retrieval digest only; no automated semantic classification.','']
    current_filing=None; current_fam=None; buckets={}
    for line in lines[1:]:
        if line.startswith('## '): current_filing=line; buckets.setdefault(current_filing,{f:[] for f in WEIGHTS})
        elif line.startswith('### '): current_fam=line[4:].strip()
        elif line.startswith('- ') and current_filing and current_fam in WEIGHTS:
            p=line[2:].strip(); buckets[current_filing][current_fam].append((score(p,current_fam),p))
    for filing,fams in buckets.items():
        out += [filing,'']
        for fam,vals in fams.items():
            vals=sorted(vals,key=lambda x:(-x[0],x[1]))[:8]
            out.append('### '+fam)
            if not vals: out.append('- NONE')
            for s,p in vals: out.append(f'- [{s:.1f}] {p}')
            out.append('')
    return '\n'.join(out)+'\n'
def main():
    files=sorted(p for p in SRC.glob('[0-9][0-9][0-9]_*.md'))
    for p in files: (OUT/p.name).write_text(parse(p),encoding='utf-8')
    (OUT/'digest_status.json').write_text(json.dumps({'digests':len(files)},indent=2)+'\n')
    print(json.dumps({'digests':len(files)}))
if __name__=='__main__':main()
