import csv, json, hashlib, pathlib
from collections import Counter, defaultdict

ROOT=pathlib.Path(__file__).resolve().parent
SC=ROOT/'t0_scoring'
OUT=SC
MAN=ROOT/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'

pred_files=[SC/f'H06_T0_COMPANY_PREDICTOR_LEDGER_BATCH{i:02d}_FROZEN.csv' for i in range(1,12)]
for p in pred_files:
    assert p.exists(), f'MISSING PREDICTOR LEDGER: {p.name}'

# Normalize company predictor ledgers without changing any semantic call.
preds=[]
for batch,p in enumerate(pred_files,1):
    for r in csv.DictReader(p.open(encoding='utf-8')):
        nr={
            'sample_order':int(r['sample_order']),
            'sector':r.get('sector',''),
            'ticker':r.get('ticker',''),
            'company_name':r.get('company_name',''),
            'F5_class':r.get('F5_class') or r.get('F5_primary_classification') or '',
            'F5_strength':r.get('F5_strength') or r.get('F5_signal_strength') or '',
            'H06_intensity_binary':r.get('H06_intensity_binary',''),
            'semantic_acceleration':r.get('semantic_acceleration',''),
            'affected_actor':r.get('affected_actor',''),
            'trajectory_rationale':r.get('trajectory_rationale',''),
            'scorer_confidence':r.get('scorer_confidence',''),
            'batch_number':f'{batch:02d}',
            'batch_status':r.get('batch_status','FROZEN_WITHIN_BATCH_PRE_OUTCOME'),
        }
        preds.append(nr)

preds.sort(key=lambda r:r['sample_order'])
assert len(preds)==225, f'company rows={len(preds)}'
assert [r['sample_order'] for r in preds]==list(range(1,226)), 'sample_order not exactly 1..225'
assert len({r['ticker'] for r in preds})==225, 'duplicate ticker in predictor master'
assert Counter(r['H06_intensity_binary'] for r in preds)==Counter({'LOW':169,'HIGH':56}), Counter(r['H06_intensity_binary'] for r in preds)
assert Counter(r['semantic_acceleration'] for r in preds)==Counter({'NO':214,'YES':11}), Counter(r['semantic_acceleration'] for r in preds)

pred_fields=['sample_order','sector','ticker','company_name','F5_class','F5_strength','H06_intensity_binary','semantic_acceleration','affected_actor','trajectory_rationale','scorer_confidence','batch_number','batch_status']
pred_csv=OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_FROZEN.csv'
with pred_csv.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=pred_fields); w.writeheader(); w.writerows(preds)
(OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_FROZEN.json').write_text(json.dumps(preds,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

manifest=list(csv.DictReader(MAN.open(encoding='utf-8')))
assert len(manifest)==1125, f'manifest rows={len(manifest)}'
by_order=defaultdict(list)
for r in manifest: by_order[int(r['sample_order'])].append(r)
assert set(by_order)==set(range(1,226)), 'manifest sample orders not 1..225'
for order,rs in by_order.items():
    assert len(rs)==5, f'{order}: filing count {len(rs)}'
    assert sorted(r['filing_position'] for r in rs)==['F1','F2','F3','F4','F5'], f'{order}: bad positions'
assert len({(r['sample_order'],r['accession_number']) for r in manifest})==1125, 'duplicate company/accession pairs in manifest'

# Merge already-persisted filing-level ledgers for Batches 01-08, preserving their frozen fields.
signal_files=sorted(SC.glob('H06_T0_SIGNAL_LEDGER_WORKING_BATCH0[1-8]_*.csv'))
assert len(signal_files)==8, f'expected 8 persisted filing ledgers; got {len(signal_files)}'
legacy=[]
for p in signal_files:
    for r in csv.DictReader(p.open(encoding='utf-8')):
        legacy.append(r)
assert len(legacy)==920, f'persisted filing rows={len(legacy)}'

manifest_key={(int(r['sample_order']),r['filing_position']):r for r in manifest}
legacy_key=set()
for r in legacy:
    k=(int(r['sample_order']),r['filing_position'])
    assert k in manifest_key, f'legacy row absent from manifest: {k}'
    m=manifest_key[k]
    assert r.get('ticker')==m['ticker'], f'ticker mismatch {k}'
    assert r.get('form')==m['form'], f'form mismatch {k}'
    assert r.get('filing_date')==m['filing_date'], f'date mismatch {k}'
    assert r.get('accession_number')==m['accession_number'], f'accession mismatch {k}'
    legacy_key.add(k)
assert len(legacy_key)==920, 'duplicates in persisted filing ledgers'
assert legacy_key=={(int(r['sample_order']),r['filing_position']) for r in manifest if int(r['sample_order'])<=184}, 'Batch01-08 coverage mismatch'

# Canonical 1,125-row signal ledger: start from manifest, attach frozen company trajectory predictors to every filing,
# and preserve per-filing semantic fields where a separate Batch01-08 filing ledger actually exists.
pred_by_order={r['sample_order']:r for r in preds}
legacy_by_key={(int(r['sample_order']),r['filing_position']):r for r in legacy}
rows=[]
for m in sorted(manifest,key=lambda r:(int(r['sample_order']),int(r['filing_position'][1:]))):
    order=int(m['sample_order']); k=(order,m['filing_position']); p=pred_by_order[order]; old=legacy_by_key.get(k)
    row=dict(m)
    row.update({
        'F5_class':p['F5_class'],
        'F5_strength':p['F5_strength'],
        'H06_intensity_binary':p['H06_intensity_binary'],
        'semantic_acceleration':p['semantic_acceleration'],
        'company_affected_actor':p['affected_actor'],
        'trajectory_rationale':p['trajectory_rationale'],
        'batch_number':p['batch_number'],
        'company_predictor_status':p['batch_status'],
        'filing_classification': old.get('classification','') if old else '',
        'filing_signal_strength': old.get('signal_strength','') if old else '',
        'filing_temporal_state': old.get('temporal_state','') if old else '',
        'filing_affected_actor': old.get('affected_actor','') if old else '',
        'filing_origin_status': old.get('origin_status','') if old else '',
        'filing_evidence': (old.get('evidence_summary') or old.get('evidence_passage') or '') if old else '',
        'filing_specificity': old.get('specificity','') if old else '',
        'filing_novelty': old.get('novelty','') if old else '',
        'filing_persistence': old.get('persistence','') if old else '',
        'filing_commercial_explicitness': old.get('commercial_explicitness','') if old else '',
        'filing_scorer_confidence': old.get('scorer_confidence','') if old else '',
        'filing_row_source': 'PERSISTED_FROZEN_BATCH_FILING_LEDGER' if old else 'FROZEN_MANIFEST_PLUS_COMPANY_TRAJECTORY_ONLY',
    })
    rows.append(row)
assert len(rows)==1125
assert Counter(r['filing_row_source'] for r in rows)==Counter({'PERSISTED_FROZEN_BATCH_FILING_LEDGER':920,'FROZEN_MANIFEST_PLUS_COMPANY_TRAJECTORY_ONLY':205})

signal_fields=list(manifest[0].keys())+['F5_class','F5_strength','H06_intensity_binary','semantic_acceleration','company_affected_actor','trajectory_rationale','batch_number','company_predictor_status','filing_classification','filing_signal_strength','filing_temporal_state','filing_affected_actor','filing_origin_status','filing_evidence','filing_specificity','filing_novelty','filing_persistence','filing_commercial_explicitness','filing_scorer_confidence','filing_row_source']
sig_csv=OUT/'H06_T0_SIGNAL_LEDGER_FROZEN.csv'
with sig_csv.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=signal_fields); w.writeheader(); w.writerows(rows)
(OUT/'H06_T0_SIGNAL_LEDGER_FROZEN.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Integrity check that company predictors align with manifest identities.
for order,rs in by_order.items():
    p=pred_by_order[order]
    assert all(r['ticker']==p['ticker'] for r in rs), f'predictor/manifest ticker mismatch {order}'

freeze=OUT/'H06_T0_FINAL_FREEZE_RECORD.md'
freeze.write_text(f'''# H06 T0 Final Freeze Record\n\n**Date:** 18 August 2026\n**Status:** FROZEN — READY FOR 24-MONTH OUTCOME AUDIT\n\n## Verified integrity\n\n- T0 semantic scoring is complete and company predictors are frozen.\n- Companies: **225**\n- Exact frozen F1–F5 filings: **1,125**\n- Sample orders: **1–225, no gaps**\n- Exactly five filings per company: **YES**\n- Filing positions F1–F5 exactly once per company: **YES**\n- Duplicate company/accession pairs: **0**\n- Every filing matches `H06_SAMPLE_MANIFEST_FROZEN.csv`: **YES**\n- High Signal Intensity: **56**\n- Low Signal Intensity: **169**\n- Semantic Acceleration YES: **11**\n- Semantic Acceleration NO: **214**\n- Post-F5 outcome information used: **NONE**\n\n## Mechanical consolidation note\n\nBatches 01–08 had separately persisted filing-level T0 ledgers covering **920 filings**. Batches 09–11 had frozen company-level predictor ledgers but no separately persisted filing-level semantic ledgers. To avoid retroactive rescoring, the remaining **205 filing rows** were reconstructed mechanically from the already-frozen SEC manifest and linked to their already-frozen company-level F5 intensity/acceleration predictors. No per-filing semantic labels were invented for those 205 rows; their legacy per-filing fields are intentionally blank and `filing_row_source` records this distinction.\n\nThis is a documentation/consolidation correction only. It changes **zero** frozen High/Low calls and **zero** frozen Semantic Acceleration calls.\n\n## Freeze gate\n\nAll company-level predictors are now locked. H06 is ready to open the preregistered 24-month outcome audit. Outcome research must use the frozen predictors without modification.\n''',encoding='utf-8')

artifacts=[pred_csv,OUT/'H06_T0_COMPANY_PREDICTOR_LEDGER_FROZEN.json',sig_csv,OUT/'H06_T0_SIGNAL_LEDGER_FROZEN.json',freeze]
checks=OUT/'H06_T0_MASTER_CHECKSUMS.txt'
with checks.open('w',encoding='utf-8') as f:
    for p in artifacts:
        f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')

status={
 'master_t0_frozen':True,'companies':225,'filings':1125,'high':56,'low':169,'acceleration_yes':11,'acceleration_no':214,
 'persisted_filing_semantic_rows':920,'mechanically_reconstructed_manifest_rows_without_new_semantic_labels':205,
 'outcome_research':'CLOSED_DURING_T0_CONSOLIDATION','ready_for_24_month_outcome_audit':True
}
(OUT/'H06_T0_MASTER_FREEZE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status,indent=2))
