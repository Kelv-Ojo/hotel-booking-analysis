from pathlib import Path
import openpyxl,json,collections
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('workbook',type=Path)
args=parser.parse_args()
b=openpyxl.load_workbook(args.workbook,read_only=True,data_only=True)
s=b['hotel_bookings'].iter_rows(values_only=True);h=next(s)
rows=[dict(zip(h,v)) for v in s]
july=[r for r in rows if r['arrival_date_year']==2015 and r['arrival_date_month']=='July']
# Transcribed from native report screenshots, before the presentation-only label edits.
checked={(0,2):2,(1,0):99,(1,1):26,(1,2):38,(1,3):1,(1,4):3,(2,0):455,(2,1):220,(2,2):493,(2,3):35,(2,4):53,(2,5):1,(3,0):29,(3,1):23,(3,2):31,(3,3):2,(3,4):4,(4,0):1,(4,1):1}
flags={(1,0):30,(1,1):18,(1,2):17,(1,3):3,(1,4):1,(1,5):3,(2,0):487,(2,1):272,(2,2):373,(2,3):20,(2,4):13,(2,6):1,(3,0):7,(3,1):9,(3,2):4,(3,4):1}
for label,pred,observed in [('checked_out',lambda r:r['reservation_status']=='Check-Out',checked),('cancellation_flags',lambda r:r['is_canceled']==1,flags)]:
 expected=dict(collections.Counter((r['adults'],r['stays_in_weekend_nights']) for r in july if pred(r)))
 assert expected==observed,(label,expected,observed)
assert sum(checked.values())==1517 and sum(flags.values())==1259
checks={'date_range_July2015':{'bookings':2776,'checked_out':1517,'flags':1259},'MonthYear_July2015':{'bookings':2776,'checked_out':1517,'flags':1259},'PRT2016':{'bookings':22321,'flags':12405},'Direct_PRT2016':{'bookings':2652,'flags':513},'Direct2016':{'bookings':5663,'flags':867},'July_NoDeposit_chart_selection':{'checked_out':1517,'flags':1029},'july_matrix_cells':{'checked_out_cells':len(checked),'flag_cells':len(flags),'all_nonempty_cells_match':True}}
for key,pred in [('PRT2016',lambda r:r['arrival_date_year']==2016 and r['country']=='PRT'),('Direct_PRT2016',lambda r:r['arrival_date_year']==2016 and r['country']=='PRT' and r['market_segment']=='Direct'),('Direct2016',lambda r:r['arrival_date_year']==2016 and r['market_segment']=='Direct')]:
 rs=[r for r in rows if pred(r)];assert len(rs)==checks[key]['bookings'];assert sum(r['is_canceled'] for r in rs)==checks[key]['flags']
# Rate labels are rounded by the report to one decimal place.
for col,observed in [('adults',{'0':0.0,'1':30.1,'2':48.1,'3':19.1,'4':0.0}),('customer_type',{'Group':0.0,'Transient':35.0,'Transient-Party':55.6,'Contract':62.3})]:
 for group,rate in observed.items():
  rs=[r for r in july if str(r[col])==group];got=round(100*sum(r['is_canceled'] for r in rs)/len(rs),1);assert got==rate,(col,group,got,rate)
rs=[r for r in july if r['deposit_type']=='No Deposit'];assert sum(r['is_canceled'] for r in rs)==1029
print('Verified native matrix cells, rate labels, slicer scopes and deposit totals against the original workbook.')
