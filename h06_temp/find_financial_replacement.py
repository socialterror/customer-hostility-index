import csv,hashlib,io,json,urllib.request
import verify_manifest as vm

CUTOFF='2020-11-30'; SEED='H06-2026-08-18-v1'
SOURCE='https://raw.githubusercontent.com/lawcal/sp500-components-history/main/data/components_history.csv'
H04=set('GPRO SONO YETI SSTK EB ALRM GRPN VRM NTNX PSTG DOMO MNTV BL APPF PAYC PCTY SPT FUBO SIX SEAS'.split())
H05=set('ETR CSX MU DELL MMM GIS UBER GLW EA ISRG AMGN TTD TT TEL JKHY ATO TMUS ES LITE DLTR NCLH WDAY JNJ HAL APD MO AOS MPC SPGI PWR CHRW VZ HON NEE CVX SNA AZO GE KR ROK GPC EFX AAPL GM AME DVA VEEV A DE CCL BBY LUV STX TXN YUM HSIC EXPD NWSA ON MDLZ BALL FISV DXCM TTWO INCY SLB ECL VST VRTX FCX FDS NRG NOW CTAS CVNA'.split())
EXPECTED_TOP36='USB GS UNM FITB MS AJG AMP SCHW CBOE L FLT RF HBAN TRV PYPL BAC MA MET FRC PRU SIVB FIS PFG AIZ MKTX AFL C DFS STT AON GL CFG PBCT RJF TROW NDAQ'.split()

def clean_date(x): return (x or '').replace('*','').strip()
def active(row):
    a=clean_date(row['date_added']); r=clean_date(row['date_removed'])
    return bool(a) and a<=CUTOFF and (not r or r>CUTOFF)
def rankkey(cik): return hashlib.sha256(f'{SEED}|{cik.zfill(10)}'.encode()).hexdigest()

def main():
    req=urllib.request.Request(SOURCE,headers={'User-Agent':'CHI H06 manifest research'})
    raw=urllib.request.urlopen(req,timeout=60).read().decode('utf-8-sig')
    rows=list(csv.DictReader(io.StringIO(raw)))
    active_rows=[r for r in rows if active(r) and r.get('cik','').strip()]
    # one issuer/CIK, lexicographically smallest ticker; exactly as frozen addendum
    by={}
    for r in active_rows:
        cik=r['cik'].strip().zfill(10); sym=r['symbol'].strip()
        if cik not in by or sym<by[cik]['symbol']: by[cik]=r
    issuers=[]
    for cik,r in by.items():
        sym=r['symbol'].strip()
        if sym in H04 or sym in H05: continue
        issuers.append({'ticker':sym,'CIK':cik,'company':r['name'].strip(),'sector':r['sector'].strip()})
    financials=[r for r in issuers if r['sector']=='financials']
    financials.sort(key=lambda r:rankkey(r['CIK']))
    got=[r['ticker'] for r in financials[:36]]
    if got!=EXPECTED_TOP36:
        raise RuntimeError('reconstructed financial ranking does not match frozen top-36; refusing replacement\nGOT='+str(got))
    byidx,_=vm.build_index()
    attempts=[]
    for rank,r in enumerate(financials[36:],start=37):
        five,err=vm.choose(byidx.get(r['CIK'],[]))
        attempts.append({'rank':rank,**r,'eligible':err is None,'reason':err or 'PASS'})
        if err is None:
            result={'status':'PASS','replacement_for':'FRC','replacement_rank':rank,**r,
                    'filings':[{'position':f'F{i}','form':x['form'],'filing_date':x['filing_date'],'accession_number':x['accession_number'],'sec_locator':x['sec_locator']} for i,x in enumerate(five,1)],
                    'attempts':attempts}
            (vm.OUT/'H06_FRC_REPLACEMENT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result,indent=2)); return
    raise RuntimeError('no valid same-sector replacement found')

if __name__=='__main__': main()
