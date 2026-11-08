"""Render the verified complete-year comparison for the recording."""
from pathlib import Path
import csv, calendar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
with (root/'reports/monthly.csv').open() as f:
    rows=[r for r in csv.DictReader(f) if r['year_month'].startswith('2016-')]
fig,axes=plt.subplots(2,1,figsize=(12,7),sharex=True,layout='constrained')
for ax,hotel in zip(axes,['City Hotel','Resort Hotel']):
    selected=sorted((r for r in rows if r['hotel']==hotel),key=lambda r:r['year_month'])
    assert len(selected)==12 and len({r['year_month'] for r in selected})==12
    checked=[int(r['checked_out']) for r in selected]
    canceled=[int(r['canceled']) for r in selected]
    total=[int(r['bookings']) for r in selected]
    assert all(a+b==c for a,b,c in zip(checked,canceled,total))
    peak=max(range(12),key=total.__getitem__)
    ax.bar(range(1,13),checked,label='Checked out',color='#276749')
    ax.bar(range(1,13),canceled,bottom=checked,label='Cancellation flag (includes no-shows)',color='#a03b39')
    ax.annotate(f'October: {total[peak]:,} bookings',xy=(peak+1,total[peak]),xytext=(7,total[peak]*1.12),arrowprops={'arrowstyle':'->','color':'#333333'})
    ax.set_ylim(0,max(total)*1.3);ax.set_title(hotel,loc='left');ax.set_ylabel('Booking records')
    ax.spines[['top','right']].set_visible(False)
axes[0].legend(loc='upper left',frameon=False)
axes[1].set_xticks(range(1,13),[calendar.month_abbr[m] for m in range(1,13)])
axes[1].set_xlabel('Scheduled arrival month, 2016')
fig.suptitle('October had the most bookings at both hotels in 2016',fontsize=17)
out=root/'assets/screenshots/peak-month-2016.png';out.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(out,dpi=150);plt.close(fig)
print(out)
