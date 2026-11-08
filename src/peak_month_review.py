"""Compare complete-year booking peaks; source is the verified monthly output."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'reports/monthly.csv').open(encoding='utf-8')))
findings=[]
for hotel in sorted({r['hotel'] for r in rows}):
 selected=[r for r in rows if r['hotel']==hotel and r['year_month'].startswith('2016-')]
 assert len(selected)==12 and len({r['year_month'] for r in selected})==12
 assert all(int(r['canceled'])+int(r['checked_out'])==int(r['bookings']) for r in selected)
 peak=max(selected,key=lambda r:int(r['bookings']))
 findings.append({'hotel':hotel,'peak_arrival_month':peak['year_month'],'bookings':int(peak['bookings']),'cancellation_flags':int(peak['canceled']),'checked_out':int(peak['checked_out']),'annual_bookings':sum(int(r['bookings']) for r in selected)})
(ROOT/'reports/peak_month_2016.json').write_text(json.dumps(findings,indent=2)+'\n',encoding='utf-8')
print(json.dumps(findings,indent=2))
