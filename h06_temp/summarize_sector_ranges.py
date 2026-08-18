import csv,json,pathlib
root=pathlib.Path(__file__).resolve().parent
p=root/'output'/'H06_SAMPLE_MANIFEST_FROZEN.csv'
by={}
with p.open(newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        o=int(r['sample_order']); s=r['sector']
        by.setdefault(s,set()).add(o)
out={s:{'start':min(v),'end':max(v),'companies':len(v),'filings':len(v)*5} for s,v in by.items()}
(root/'output'/'H06_SECTOR_ORDER_RANGES.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))