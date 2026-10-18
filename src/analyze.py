"""Build a relational hotel reporting model and independently reconcile outputs."""
from pathlib import Path
import json,sqlite3,zipfile,calendar
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'reports';out.mkdir(exist_ok=True)
    with zipfile.ZipFile(ROOT/'data/bookings.csv.zip') as z:
        with z.open('bookings.csv') as f: df=pd.read_csv(f,keep_default_na=False)
    assert df.source_row.is_unique
    assert len(df)==119390, 'Unexpected source snapshot; inspect before updating'
    assert df.is_canceled.isin([0,1]).all() and df.lead_time.ge(0).all()
    months={m:i for i,m in enumerate(calendar.month_name) if m}
    df['arrival_date']=pd.to_datetime(dict(year=df.arrival_date_year,month=df.arrival_date_month.map(months),day=df.arrival_date_day_of_month)).dt.strftime('%Y-%m-%d')
    df['year_month']=df.arrival_date.str[:7]
    df['year']=df.arrival_date_year.astype(int)
    db_path=ROOT/'reports/hotel.db'
    if db_path.exists():db_path.unlink()
    with sqlite3.connect(db_path) as db:
        db.executescript((ROOT/'sql/schema.sql').read_text())
        for col,table,key,label in [('hotel','hotels','hotel_id','hotel'),('distribution_channel','channels','channel_id','channel'),('market_segment','segments','segment_id','segment')]:
            values=sorted(df[col].unique());mapping={v:i+1 for i,v in enumerate(values)}
            db.executemany(f'INSERT INTO {table} VALUES (?,?)',[(i,v) for v,i in mapping.items()]);df[key]=df[col].map(mapping)
        dates=pd.date_range(df.arrival_date.min(),df.arrival_date.max())
        db.executemany('INSERT INTO dates VALUES (?,?,?,?)',[(d.strftime('%Y-%m-%d'),d.year,d.month,d.strftime('%Y-%m')) for d in dates])
        cols=['source_row','hotel_id','channel_id','segment_id','arrival_date','is_canceled','lead_time','customer_type','deposit_type','reservation_status']
        db.executemany('INSERT INTO bookings VALUES (?,?,?,?,?,?,?,?,?,?)',df[cols].itertuples(index=False,name=None))
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
        for name in ['monthly','segments','quality']:
            result=pd.read_sql_query((ROOT/f'sql/{name}.sql').read_text(),db)
            result.to_csv(out/f'{name}.csv',index=False)
            if name=='monthly': monthly=result
            if name=='quality': assert result.issue_count.sum()==0
        joined=db.execute('SELECT COUNT(*) FROM bookings b JOIN hotels h ON h.hotel_id=b.hotel_id JOIN channels c ON c.channel_id=b.channel_id JOIN segments s ON s.segment_id=b.segment_id JOIN dates d ON d.date_id=b.arrival_date').fetchone()[0]
        assert joined==len(df)
        model=out/'model';model.mkdir(exist_ok=True)
        for table in ['bookings','hotels','channels','segments','dates']:
            pd.read_sql_query(f'SELECT * FROM {table}',db).to_csv(model/f'{table}.csv',index=False)
    assert monthly.bookings.sum()==len(df)
    assert monthly.canceled.sum()==df.is_canceled.sum()
    independent=df.groupby(['year_month','hotel']).is_canceled.agg(['size','sum']).sort_index()
    sql_result=monthly.set_index(['year_month','hotel']).sort_index()
    assert (independent['size'].to_numpy()==sql_result.bookings.to_numpy()).all()
    assert (independent['sum'].to_numpy()==sql_result.canceled.to_numpy()).all()
    # Compact source table for Excel: all bookings represented, no row sampling.
    df['checked_out']=df.reservation_status.eq('Check-Out').astype(int)
    df['no_show']=df.reservation_status.eq('No-Show').astype(int)
    excel=df.groupby(['year','year_month','hotel','distribution_channel'],as_index=False).agg(bookings=('source_row','size'),canceled=('is_canceled','sum'),checked_out=('checked_out','sum'),no_shows=('no_show','sum'))
    excel.to_csv(out/'excel_source.csv',index=False)
    (ROOT/'excel/source.json').write_text(excel.to_json(orient='values'))
    hotels=df.groupby('hotel').is_canceled.agg(['size','sum'])
    metrics={'bookings':len(df),'canceled':int(df.is_canceled.sum()),'cancellation_rate':float(df.is_canceled.mean()),'start':df.arrival_date.min(),'end':df.arrival_date.max(),'checked_out':int(df.checked_out.sum()),'no_shows':int(df.no_show.sum()),'excel_aggregate_rows':len(excel),'join_rows':joined,'hotel_rates':{h:float(r['sum']/r['size']) for h,r in hotels.iterrows()}}
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    findings=f'''# Hotel booking findings

The full source snapshot contains **{len(df):,} bookings**, arriving from **{metrics['start']} to {metrics['end']}**. **{metrics['canceled']:,} ({metrics['cancellation_rate']:.1%})** have the source cancellation flag. This flag includes no-shows; {metrics['no_shows']:,} are labelled No-Show and {metrics['checked_out']:,} Check-Out.

## Findings and recommended investigation

- City Hotel cancellation flag rate: **{metrics['hotel_rates']['City Hotel']:.1%}**; Resort Hotel: **{metrics['hotel_rates']['Resort Hotel']:.1%}**. Investigate channel and lead-time mix before attributing the difference to hotel operations.
- Examine high-volume segments in `segments.csv` for targeted confirmation or communication trials. Rate rankings exclude groups below 100 bookings but do not adjust for confounding.
- Compare matching months across years. The dataset starts in July 2015 and ends in August 2017, so whole-year totals are not directly comparable. Month-to-month changes are descriptive and seasonal.

## Reporting corrections and limits

The original Power BI PDF shows 36,483 in its YTD card, a different scope from the full 119,390-row source; these must not be described as the same population. Its date axis includes 2014, while source arrival dates begin in July 2015. The original PBIX and PDF are preserved as earlier work; they have not been repaired or reopened in Power BI Desktop here. Use the verified SQL outputs and Excel report for full-snapshot metrics.

Do not call all non-canceled bookings completed stays. Use the explicit reservation_status='Check-Out' count for checked-out bookings, and label the cancellation flag as including no-shows. A booking is not necessarily a distinct guest. Repeated identical business fields can represent distinct bookings; no deduplication was performed without a source booking ID. Added booking IDs are original workbook row numbers, not business-issued IDs.

No room inventory, costs, payment transactions or treatment data is supplied. Occupancy, profit, realized revenue and causal effects cannot be established. No current hotel performance or savings is claimed. All recommendations are proposed investigations, not implemented outcomes.

## Verification

119,390 source rows retained; primary and foreign keys verified; dimension joins preserve row count; SQL totals reconcile to pandas for every month and hotel; no status/flag mismatches. The Excel source represents the complete dataset aggregated by arrival month, hotel and channel.
'''
    (out/'findings.md').write_text(findings)
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':main()
