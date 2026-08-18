import csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
src=ROOT/'t0_review'/'batch07_industrials_compact.tsv'; out=ROOT/'t0_review'/'batch07_split'; out.mkdir(exist_ok=True)
rows=list(csv.DictReader(src.open(encoding='utf-8'),delimiter='\t'))
for r in rows:
    p=out/f"{int(r['order']):03d}_{r['ticker']}.md"
    p.write_text(f"# {int(r['order']):03d} {r['ticker']}\n\n## F1\n{r['F1_best']}\n\n## F5\n{r['F5_best']}\n\n## MID\n{r['mid_best']}\n",encoding='utf-8')
print('split',len(rows))
