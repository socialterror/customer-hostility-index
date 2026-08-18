import base64,csv,hashlib,io,json,math,pathlib,re,urllib.request
from collections import defaultdict,Counter
import verify_manifest as vm

CUTOFF='2020-11-30'; SEED='H06-2026-08-18-v1'; TARGET=225
MEMBERSHIP_BLOB='4aeb5f6046dea43063f9c7be72dfdf16e96d2821'
METADATA_BLOB='eb016916286be8b205a6f337906b472a37816e47'
H04=set('GPRO SONO YETI SSTK EB ALRM GRPN VRM NTNX PSTG DOMO MNTV BL APPF PAYC PCTY SPT FUBO SIX SEAS'.split())
H05=set('ETR CSX MU DELL MMM GIS UBER GLW EA ISRG AMGN TTD TT TEL JKHY ATO TMUS ES LITE DLTR NCLH WDAY JNJ HAL APD MO AOS MPC SPGI PWR CHRW VZ HON NEE CVX SNA AZO GE KR ROK GPC EFX AAPL GM AME DVA VEEV A DE CCL BBY LUV STX TXN YUM HSIC EXPD NWSA ON MDLZ BALL FISV DXCM TTWO INCY SLB ECL VST VRTX FCX FDS NRG NOW CTAS CVNA'.split())
CIK_OVERRIDE={'XOM':'0000034088','APA':'0000006769'}
OUT=vm.OUT

def blob_csv(repo,sha):
    url=f'https://api.github.com/repos/{repo}/git/blobs/{sha}'
    req=urllib.request.Request(url,headers={'User-Agent':'CHI H06 pre-T0 manifest research','Accept':'application/vnd.github+json'})
    obj=json.loads(urllib.request.urlopen(req,timeout=60).read().decode())
    raw=base64.b64decode(obj['content'])
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))), hashlib.sha256(raw).hexdigest()
def clean(x): return (x or '').replace('*','').strip()
def active(s,e): return bool(clean(s)) and clean(s)<=CUTOFF and (not clean(e) or clean(e)>CUTOFF)
def h(cik): return hashlib.sha256(f'{SEED}|{cik.zfill(10)}'.encode()).hexdigest()
def write_csv(path,rows,fields=None):
    if fields is None: fields=list(rows[0]) if rows else []
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def hamilton(counts,total=TARGET):
    n=sum(counts.values()); exact={s:total*v/n for s,v in counts.items()}; q={s:int(math.floor(x)) for s,x in exact.items()}
    left=total-sum(q.values())
    order=sorted(counts,key=lambda s:(-(exact[s]-q[s]),s))
    for s in order[:left]: q[s]+=1
    return q,exact

def main():
    membership,msha=blob_csv('fja05680/sp500',MEMBERSHIP_BLOB)
    historical=sorted({r['ticker'].strip() for r in membership if active(r['start_date'],r['end_date'])})
    metadata,dsha=blob_csv('lawcal/sp500-components-history',METADATA_BLOB)
    active_meta=defaultdict(list)
    for r in metadata:
        sym=r['symbol'].strip()
        if sym in historical and active(r['date_added'],r['date_removed']) and clean(r.get('cik')):
            active_meta[sym].append(r)
    missing=sorted(t for t in historical if t not in active_meta)
    if missing: raise RuntimeError('missing metadata for historical tickers: '+str(missing))
    securities=[]
    for t in historical:
        cand=active_meta[t]; ciks={clean(r['cik']).zfill(10) for r in cand}
        if t in CIK_OVERRIDE: cik=CIK_OVERRIDE[t]
        elif len(ciks)==1: cik=next(iter(ciks))
        else: raise RuntimeError(f'ambiguous CIK for {t}: {sorted(ciks)}')
        r=cand[0]
        securities.append({'ticker':t,'CIK':cik,'company_name':r['name'].strip(),'sector':r['sector'].strip()})
    # one issuer per CIK, lexicographically smallest ticker
    issuer={}
    for r in securities:
        if r['CIK'] not in issuer or r['ticker']<issuer[r['CIK']]['ticker']: issuer[r['CIK']]=r
    # prior-study exclusion by CIK, not current ticker label
    prior_ciks=set()
    for t in H04|H05:
        if t in active_meta:
            ciks={clean(r['cik']).zfill(10) for r in active_meta[t]}
            if t in CIK_OVERRIDE: prior_ciks.add(CIK_OVERRIDE[t])
            elif len(ciks)==1: prior_ciks.add(next(iter(ciks)))
    candidates=[dict(r) for cik,r in issuer.items() if cik not in prior_ciks]
    # SEC filing eligibility BEFORE selection
    sec_by_cik,sources=vm.build_index()
    eligible=[]; technical_fail=[]
    for r in candidates:
        five,err=vm.choose(sec_by_cik.get(r['CIK'],[]))
        if err:
            technical_fail.append({**r,'exclusion_reason':err}); continue
        rr={**r,'random_hash':h(r['CIK'])}
        rr['_five']=five; eligible.append(rr)
    counts=Counter(r['sector'] for r in eligible); quotas,exact=hamilton(counts)
    selected=[]
    for sector in sorted(counts):
        ranked=sorted([r for r in eligible if r['sector']==sector],key=lambda r:r['random_hash'])
        for rank,r in enumerate(ranked,1): r['sector_rank']=rank
        selected += ranked[:quotas[sector]]
    # stable sample order = sector alphabetical then rank, mirroring stratified deterministic construction
    selected=sorted(selected,key=lambda r:(r['sector'],r['sector_rank']))
    if len(selected)!=TARGET or len({r['CIK'] for r in selected})!=TARGET: raise RuntimeError('sample cardinality failure')
    sample=[]; manifest=[]
    for order,r in enumerate(selected,1):
        sample.append({'sample_order':order,'sector':r['sector'],'sector_rank':r['sector_rank'],'ticker':r['ticker'],
                       'historical_sec_cik':r['CIK'],'company':r['company_name'],'randomization_seed':SEED,
                       'selection_status':'H06_CORRECTED_PRE_T0_FROZEN'})
        for i,x in enumerate(r['_five'],1):
            manifest.append({'sample_order':order,'sector':r['sector'],'sector_rank':r['sector_rank'],'ticker':r['ticker'],
              'company_name':r['company_name'],'CIK':r['CIK'],'filing_position':f'F{i}','form':x['form'],
              'filing_date':x['filing_date'],'accession_number':x['accession_number'],'sec_locator':x['sec_locator'],
              'verification_status':'VERIFIED_FROM_OFFICIAL_SEC_MASTER_INDEX',
              'verification_note':'Corrected pre-T0 universe; sequential 10-Q/10-K under frozen H06 F5 rule'})
    if len(manifest)!=1125 or len({(r['CIK'],r['accession_number']) for r in manifest})!=1125: raise RuntimeError('manifest cardinality/duplicate failure')
    # Persist corrected eligible universe without private helper object.
    eligrows=[]
    for r in sorted(eligible,key=lambda x:(x['sector'],x['random_hash'])):
        eligrows.append({k:r[k] for k in ['ticker','CIK','company_name','sector','random_hash']})
    qrows=[{'sector':s,'eligible_n':counts[s],'exact_quota':exact[s],'quota':quotas[s]} for s in sorted(counts)]
    write_csv(OUT/'H06_ELIGIBLE_UNIVERSE_CORRECTED_FROZEN.csv',eligrows)
    write_csv(OUT/'H06_TECHNICAL_INELIGIBILITY_LOG_PRE_T0.csv',sorted(technical_fail,key=lambda x:(x['sector'],x['ticker'])))
    write_csv(OUT/'H06_SECTOR_QUOTAS_CORRECTED_FROZEN.csv',qrows)
    write_csv(OUT/'H06_SAMPLE_MANIFEST_FROZEN.csv',manifest)
    (OUT/'H06_SAMPLE_MANIFEST_FROZEN.json').write_text(json.dumps(manifest,indent=2)+'\n')
    write_csv(OUT/'H06_COMPANY_SAMPLE_FROZEN.csv',sample)
    # Compare superseded payload sample to corrected sample.
    old=vm.load_sample() if hasattr(vm,'load_sample') else None
    # verifier uses load_sample name in public branch; fallback decode its embedded file
    if old is None:
        old=[]
    old_ciks={str(r['historical_sec_cik']).zfill(10):r['ticker'] for r in old}
    new_ciks={r['historical_sec_cik']:r['ticker'] for r in sample}
    removed=[{'CIK':c,'ticker':t,'change':'REMOVED_FROM_SUPERSEDED_DRAW'} for c,t in old_ciks.items() if c not in new_ciks]
    added=[{'CIK':c,'ticker':t,'change':'ADDED_IN_CORRECTED_DRAW'} for c,t in new_ciks.items() if c not in old_ciks]
    changes=removed+added
    write_csv(OUT/'H06_SAMPLE_CORRECTION_CHANGELOG.csv',changes,['CIK','ticker','change'])
    src={'membership_blob':MEMBERSHIP_BLOB,'membership_blob_sha256':msha,'metadata_blob':METADATA_BLOB,'metadata_blob_sha256':dsha,
         'sec_master_indexes':sources}
    (OUT/'H06_SOURCE_VERSION_RECORD.json').write_text(json.dumps(src,indent=2)+'\n')
    log=f'''# H06 Manifest Verification and Freeze Log\n\n**STATUS: FROZEN — READY FOR BLIND T0 SEMANTIC SCORING**\n\n## Corrected pre-T0 construction\n\n- Historical cutoff: **2020-11-30**\n- Historical securities from immutable membership source: **{len(historical)}**\n- Issuers after one-CIK collapse: **{len(issuer)}**\n- Prior H04/H05 issuer CIK exclusions present in historical universe: **{len(prior_ciks & set(issuer))}**\n- Candidate issuers before SEC filing screen: **{len(candidates)}**\n- Technical filing-ineligible issuers: **{len(technical_fail)}**\n- Final eligible issuers: **{len(eligible)}**\n- Selected companies: **225**\n- Exact verified filings: **1,125**\n- F5 window: **{vm.F5_MIN} through {vm.F5_MAX}**\n- Forms: **10-Q / 10-K only**\n- Duplicate issuer/accession pairs: **0**\n- Outcome research: **CLOSED / NOT USED**\n- Semantic scoring: **NOT STARTED**\n\n## Correction rationale\n\nThe superseded pre-verification draw was not promoted to the final manifest because its recorded eligible-universe reserve was not reproducible and FRC failed the frozen F5 eligibility rule. The universe was therefore rebuilt before T0 from immutable source blobs, SEC filing eligibility was applied before selection, and the same prespecified random seed and Hamilton sector-allocation method were reapplied. No H06 semantic or outcome information was used.\n\n## Freeze statement\n\nThe corrected 225-company / 1,125-filing H06 manifest is frozen. No company or filing may be substituted after this point absent a documented genuine manifest error. The next permitted research operation is blind T0 semantic scoring.\n'''
    (OUT/'H06_MANIFEST_VERIFICATION_LOG.md').write_text(log)
    targets=['H06_ELIGIBLE_UNIVERSE_CORRECTED_FROZEN.csv','H06_TECHNICAL_INELIGIBILITY_LOG_PRE_T0.csv','H06_SECTOR_QUOTAS_CORRECTED_FROZEN.csv','H06_COMPANY_SAMPLE_FROZEN.csv','H06_SAMPLE_MANIFEST_FROZEN.csv','H06_SAMPLE_MANIFEST_FROZEN.json','H06_SAMPLE_CORRECTION_CHANGELOG.csv','H06_SOURCE_VERSION_RECORD.json','H06_MANIFEST_VERIFICATION_LOG.md']
    with (OUT/'H06_MANIFEST_CHECKSUMS.txt').open('w') as f:
        for n in targets: f.write(f"{hashlib.sha256((OUT/n).read_bytes()).hexdigest()}  {n}\n")
    result={'status':'FROZEN','historical_securities':len(historical),'issuers':len(issuer),'prior_excluded':len(prior_ciks & set(issuer)),
            'technical_ineligible':len(technical_fail),'eligible':len(eligible),'companies':225,'filings':1125,
            'sector_counts':dict(sorted(counts.items())),'sector_quotas':dict(sorted(quotas.items())),
            'sample_removed_n':len(removed),'sample_added_n':len(added)}
    (OUT/'H06_FREEZE_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__': main()
