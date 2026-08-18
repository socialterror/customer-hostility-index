import base64,csv,gzip,hashlib,io,json,pathlib,re,sys,time,urllib.request
from collections import defaultdict

ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(parents=True,exist_ok=True)
EXPECTED='5d68613b086649b6ab80fcd6f30322b8defb83ec9cd692ed741f66a040ecd059'
F5_MIN='2020-08-15'; F5_MAX='2020-11-30'; FORMS={'10-Q','10-K'}
UA='Customer Hostility Index academic research contact: jared.longhitano@gmail.com'

def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(url):
    last=None
    for i in range(5):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept-Encoding':'identity'})
            with urllib.request.urlopen(req,timeout=60) as r:
                b=r.read()
                if not b: raise RuntimeError('empty response')
                return b
        except Exception as e:
            last=e; time.sleep(2**i)
    raise RuntimeError(f'fetch failed {url}: {last}')

def load_sample():
    raw=gzip.decompress(base64.b64decode((ROOT/'sample.csv.gz.b64').read_text().strip()))
    if sha(raw)!=EXPECTED: raise RuntimeError('sample checksum mismatch')
    rows=list(csv.DictReader(io.StringIO(raw.decode())))
    if len(rows)!=225: raise RuntimeError(f'expected 225 rows, got {len(rows)}')
    c=[r['historical_sec_cik'].zfill(10) for r in rows]
    if len(set(c))!=225: raise RuntimeError('duplicate CIK in sample')
    return rows

def parse_idx(raw,url):
    lines=raw.decode('latin-1',errors='replace').splitlines(); start=None
    for i,x in enumerate(lines):
        if x.startswith('-----'): start=i+1; break
    if start is None: raise RuntimeError(f'bad master index {url}')
    out=[]
    for line in lines[start:]:
        p=line.split('|')
        if len(p)!=5: continue
        cik,name,form,dt,fn=[x.strip() for x in p]
        if form not in FORMS or not cik.isdigit(): continue
        acc=pathlib.PurePosixPath(fn).name.removesuffix('.txt')
        if not re.fullmatch(r'\d{10}-\d{2}-\d{6}',acc):
            raise RuntimeError(f'unexpected accession format {fn}')
        out.append(dict(cik=cik.zfill(10),index_name=name,form=form,filing_date=dt,
                        accession_number=acc,sec_locator='https://www.sec.gov/Archives/'+fn,source=url))
    return out

def build_index():
    by=defaultdict(list); sources=[]
    for y in (2019,2020):
        for q in (1,2,3,4):
            url=f'https://www.sec.gov/Archives/edgar/full-index/{y}/QTR{q}/master.idx'
            raw=fetch(url); sources.append({'url':url,'sha256':sha(raw),'bytes':len(raw)})
            for r in parse_idx(raw,url): by[r['cik']].append(r)
            time.sleep(.15)
    for cik,rows in by.items():
        by[cik]=sorted({r['accession_number']:r for r in rows}.values(),key=lambda x:(x['filing_date'],x['accession_number']))
    return by,sources

def choose(rows):
    candidates=[r for r in rows if F5_MIN<=r['filing_date']<=F5_MAX]
    if not candidates: return None,'no eligible F5 in frozen window'
    f5=candidates[-1]; i=rows.index(f5)
    if i<4: return None,f'only {i} preceding 10-Q/10-K filings'
    five=rows[i-4:i+1]
    if len({r['accession_number'] for r in five})!=5: return None,'duplicate accession'
    if [r['filing_date'] for r in five]!=sorted(r['filing_date'] for r in five): return None,'nonchronological sequence'
    return five,None

def write_csv(path,rows,fields=None):
    if fields is None: fields=list(rows[0]) if rows else []
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
    sample=load_sample(); by,sources=build_index(); manifest=[]; failures=[]
    for s in sample:
        cik=s['historical_sec_cik'].zfill(10); five,err=choose(by.get(cik,[]))
        if err:
            failures.append({'sample_order':s['sample_order'],'sector':s['sector'],'sector_rank':s['sector_rank'],
                             'ticker':s['ticker'],'company':s['company'],'CIK':cik,'failure_reason':err,
                             'periodic_filings_found_2019_2020':len(by.get(cik,[]))}); continue
        for n,r in enumerate(five,1):
            manifest.append({'sample_order':int(s['sample_order']),'sector':s['sector'],'sector_rank':int(s['sector_rank']),
              'ticker':s['ticker'],'company_name':s['company'],'CIK':cik,'filing_position':f'F{n}',
              'form':r['form'],'filing_date':r['filing_date'],'accession_number':r['accession_number'],
              'sec_locator':r['sec_locator'],'verification_status':'VERIFIED_FROM_OFFICIAL_SEC_MASTER_INDEX',
              'verification_note':'Sequential 10-Q/10-K under frozen H06 F5 rule'})
    failfields=['sample_order','sector','sector_rank','ticker','company','CIK','failure_reason','periodic_filings_found_2019_2020']
    write_csv(OUT/'H06_MANIFEST_FAILURES.csv',failures,failfields)
    (OUT/'H06_SEC_INDEX_SOURCE_CHECKSUMS.json').write_text(json.dumps(sources,indent=2)+'\n')
    if failures:
        write_csv(OUT/'H06_SAMPLE_MANIFEST_VERIFIED_PARTIAL.csv',manifest)
        lines=['# H06 Manifest Verification Log','','**STATUS: NOT FROZEN — TECHNICAL FAILURES REQUIRE PREREGISTERED SAME-SECTOR REPLACEMENTS**','',
               f'- Fixed sample companies tested: {len(sample)}',f'- Companies passing exact F1–F5 verification: {len(sample)-len(failures)}',
               f'- Companies failing verification: {len(failures)}',f'- Verified filing rows: {len(manifest)}','- Outcome research: CLOSED','- Semantic scoring: NOT STARTED','','## Failures']
        lines += [f"- {x['ticker']} ({x['CIK']}): {x['failure_reason']}" for x in failures]
        (OUT/'H06_MANIFEST_VERIFICATION_LOG.md').write_text('\n'.join(lines)+'\n')
        print(json.dumps({'status':'FAIL','failures':failures},indent=2)); sys.exit(2)
    if len(manifest)!=1125: raise RuntimeError(f'expected 1125 filings, got {len(manifest)}')
    if len({(r['CIK'],r['accession_number']) for r in manifest})!=1125: raise RuntimeError('duplicate issuer/accession pair')
    write_csv(OUT/'H06_SAMPLE_MANIFEST_FROZEN.csv',manifest)
    (OUT/'H06_SAMPLE_MANIFEST_FROZEN.json').write_text(json.dumps(manifest,indent=2)+'\n')
    log='''# H06 Manifest Verification Log

**STATUS: FROZEN — READY FOR BLIND T0 SEMANTIC SCORING**

- Final company count: **225**
- Exact F1–F5 filing count: **1,125**
- Five sequential periodic filings per company: **PASS**
- F5 date window 2020-08-15 through 2020-11-30: **PASS**
- Forms restricted to exact 10-Q / 10-K: **PASS**
- Duplicate issuer/accession pairs: **0**
- Frozen sample checksum: **PASS**
- Outcome research: **CLOSED / NOT USED**
- Semantic scoring: **NOT STARTED**

Every accession, form, filing date and SEC locator was derived mechanically from official SEC EDGAR quarterly master.idx files for 2019 and 2020. Source index checksums are preserved separately.

The 225-company / 1,125-filing H06 manifest is frozen. The next permitted operation is blind T0 semantic scoring under the frozen H06 preregistration.
'''
    (OUT/'H06_MANIFEST_VERIFICATION_LOG.md').write_text(log)
    targets=['H06_SAMPLE_MANIFEST_FROZEN.csv','H06_SAMPLE_MANIFEST_FROZEN.json','H06_MANIFEST_VERIFICATION_LOG.md','H06_SEC_INDEX_SOURCE_CHECKSUMS.json']
    with (OUT/'H06_MANIFEST_CHECKSUMS.txt').open('w') as f:
        f.write(f'{EXPECTED}  H06_SAMPLE_DRAW_FIXED_PRE_VERIFICATION.csv\n')
        for n in targets: f.write(f'{sha((OUT/n).read_bytes())}  {n}\n')
    print(json.dumps({'status':'FROZEN','companies':225,'filings':1125,'csv_sha256':sha((OUT/'H06_SAMPLE_MANIFEST_FROZEN.csv').read_bytes())},indent=2))

if __name__=='__main__': main()
