"""Independently compare recovered workbook and observed native DAX output."""
from pathlib import Path
import csv,io,json,zipfile,hashlib,collections
import openpyxl

import argparse
parser=argparse.ArgumentParser()
parser.add_argument('workbook',type=Path,help='Recovered original hotel source workbook')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
source=args.workbook
book=openpyxl.load_workbook(source,read_only=True,data_only=True)
stream=book['hotel_bookings'].iter_rows(values_only=True)
header=next(stream)
with zipfile.ZipFile(root/'data/bookings.csv.zip') as z:
    stored=list(csv.DictReader(io.StringIO(z.read('bookings.csv').decode())))
groups=collections.defaultdict(lambda:[0,0,0,0]);count=0
for count,values in enumerate(stream,1):
    row=dict(zip(header,values));expected=stored[count-1]
    assert int(expected['source_row'])==count+1
    for name,want in expected.items():
        if name=='source_row':continue
        got=row[name]
        assert str(got if got is not None else '')==want,(count,name,got,want)
    key=(int(row['arrival_date_year']),row['hotel'])
    g=groups[key];g[0]+=1;g[1]+=int(row['is_canceled']);g[2]+=row['reservation_status']=='Check-Out';g[3]+=row['reservation_status']=='No-Show'
assert count==len(stored)==119390
# Transcribed from executed Power BI DAX query, not generated from this source.
native=[(2015,'Resort Hotel',8314,2138,6176,69),(2015,'City Hotel',13682,6004,7678,122),(2016,'Resort Hotel',18567,4930,13637,113),(2016,'City Hotel',38140,15407,22733,555),(2017,'Resort Hotel',13179,4054,9125,109),(2017,'City Hotel',27508,11691,15817,239)]
for year,hotel,*counts in native:assert groups[year,hotel]==counts,(year,hotel)
evidence={'source_workbook_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'shared_rows_compared':count,'shared_fields_compared':len(stored[0])-1,'native_dax_comparison':'All six hotel/arrival-year scopes match independent workbook counts exactly.','columns':['year','hotel','bookings','cancellation_flags','checked_out','no_shows'],'observed_native_rows':native,'full_totals':[sum(g[i] for g in groups.values()) for i in range(4)],'scope':'Native cached-model DAX and workbook comparison. Does not certify source refresh or every visual interaction.'}
(root/'reports/native_hotel_reconciliation.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print(json.dumps(evidence,indent=2))
