import base64,csv,hashlib,io,json,urllib.request
import verify_manifest as vm

CUTOFF='2020-11-30'; SEED='H06-2026-08-18-v1'
MEMBERSHIP_BLOB='4aeb5f6046dea43063f9c7be72dfdf16e96d2821'
METADATA_BLOB='eb016916286be8b205a6f337906b472a37816e47'
H04=set('GPRO SONO YETI SSTK EB ALRM GRPN VRM NTNX PSTG DOMO MNTV BL APPF PAYC PCTY SPT FUBO SIX SEAS'.split())
H05=set('ETR CSX MU DELL MMM GIS UBER GLW EA ISRG AMGN TTD TT TEL JKHY ATO TMUS ES LITE DLTR NCLH WDAY JNJ HAL APD MO AOS MPC SPGI PWR CHRW VZ HON NEE CVX SNA AZO GE KR ROK GPC EFX AAPL GM AME DVA VEEV A DE CCL BBY LUV STX TXN YUM HSIC EXPD NWSA ON MDLZ BALL FISV DXCM TTWO INCY SLB ECL VST VRTX FCX FDS NRG NOW CTAS CVNA'.split())
EXPECTED_TOP36='USB GS UNM FITB MS AJG AMP SCHW CBOE L FLT RF HBAN TRV PYPL BAC MA MET FRC PRU SIVB FIS PFG AIZ MKTX AFL C DFS STT AON GL CFG PBCT RJF TROW NDAQ'.split()

def blob_csv(repo,sha):
    url=f'https://api.github.com/repos/{repo}/git/blobs/{sha}'
    req=urllib.request.Request(url,headers={'User-Agent':'CHI H06 manifest research','Accept':'application/vnd.github+json'})
    obj=json.loads(urllib.request.urlopen(req,timeout=60).read().decode())
    raw=base64.b64decode(obj['content']).decode('utf-8-sig')
    return list(csv.DictReader(io.StringIO(raw)))
def clean(x): return (x or '').replace('*','').strip()
def active_dates(start,end): return bool(clean(start)) and clean(start)<=CUTOFF and (not clean(end) or clean(end)>CUTOFF)
def rankkey(cik): return hashlib.sha256(f'{SEED}|{cik.zfill(10)}'.encode()).hexdigest()

def main():
    mrows=blob_csv('fja05680/sp500',MEMBERSHIP_BLOB)
    historical=[r for r in mrows if active_dates(r['start_date'],r['end_date'])]
    tickers={r['ticker'].strip() for r in historical}
    meta=blob_csv('lawcal/sp500-components-history',METADATA_BLOB)
    active_meta=[r for r in meta if r['symbol'].strip() in tickers and active_dates(r['date_added'],r['date_removed']) and clean(r.get('cik'))]
    meta_by_symbol={}
    for r in active_meta: meta_by_symbol.setdefault(r['symbol'].strip(),[]).append(r)
    missing=sorted(t for t in tickers if t not in meta_by_symbol)
    security=[]
    for t in sorted(tickers):
        cand=meta_by_symbol.get(t,[])
        if not cand: continue
        ciks={clean(r['cik']).zfill(10) for r in cand}
        if len(ciks)!=1: raise RuntimeError(f'ambiguous active CIK for {t}: {sorted(ciks)}')
        r=cand[0]; security.append({'ticker':t,'CIK':next(iter(ciks)),'company':r['name'].strip(),'sector':r['sector'].strip()})
    by={}
    for r in security:
        if r['CIK'] not in by or r['ticker']<by[r['CIK']]['ticker']: by[r['CIK']]=r
    issuers=[r for r in by.values() if r['ticker'] not in H04 and r['ticker'] not in H05]
    financials=sorted([r for r in issuers if r['sector']=='financials'],key=lambda r:rankkey(r['CIK']))
    got=[r['ticker'] for r in financials[:36]]
    diag={'membership_blob':MEMBERSHIP_BLOB,'metadata_blob':METADATA_BLOB,'historical_security_count':len(historical),
          'historical_unique_ticker_count':len(tickers),'mapped_security_count':len(security),'missing_metadata_tickers':missing,
          'issuer_count_after_CIK_collapse':len(by),'eligible_issuer_count_after_prior_exclusions':len(issuers),
          'financial_eligible_n':len(financials),'expected_top36':EXPECTED_TOP36,'reconstructed_top36':got,
          'first_50':[{'rank':i+1,**r,'hash':rankkey(r['CIK'])} for i,r in enumerate(financials[:50])]}
    (vm.OUT/'H06_FINANCIAL_RANKING_DIAGNOSTIC.json').write_text(json.dumps(diag,indent=2)+'\n')
    if missing or got!=EXPECTED_TOP36:
        raise RuntimeError('immutable-source financial ranking does not reproduce frozen top-36; refusing replacement')
    byidx,_=vm.build_index(); attempts=[]
    for rank,r in enumerate(financials[36:],start=37):
        five,err=vm.choose(byidx.get(r['CIK'],[]))
        attempts.append({'rank':rank,**r,'eligible':err is None,'reason':err or 'PASS'})
        if err is None:
            result={'status':'PASS','replacement_for':'FRC','replacement_rank':rank,**r,
              'filings':[{'position':f'F{i}','form':x['form'],'filing_date':x['filing_date'],'accession_number':x['accession_number'],'sec_locator':x['sec_locator']} for i,x in enumerate(five,1)],'attempts':attempts}
            (vm.OUT/'H06_FRC_REPLACEMENT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result,indent=2)); return
    raise RuntimeError('no valid same-sector replacement found')

if __name__=='__main__': main()
