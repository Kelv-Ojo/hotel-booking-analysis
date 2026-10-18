import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=new URL('../',import.meta.url).pathname;
const rows=JSON.parse(await fs.readFile(root+'excel/source.json','utf8'));
const metrics=JSON.parse(await fs.readFile(root+'reports/metrics.json','utf8'));
const wb=Workbook.create();
const s=wb.worksheets.add('Report');
const d=wb.worksheets.add('Monthly source');
const l=wb.worksheets.add('Definitions');
for(const sh of [s,d,l]){sh.showGridLines=false;sh.getRange('A1:N60').format.font={name:'Arial',size:10,color:'#243247'};sh.getRange('A:N').format.columnWidth=14;}
const headers=['Year','Month','Hotel','Channel','Bookings','Canceled flag','Checked out','No shows'];
d.getRange(`A1:H${rows.length+1}`).values=[headers,...rows];
d.tables.add(`A1:H${rows.length+1}`,true,'MonthlySource');
d.getRange('A1:H1').format={fill:'#263D5B',font:{bold:true,color:'#FFFFFF'}};
d.getRange('A1:B450').format.columnWidth=12;d.getRange('C1:D450').format.columnWidth=20;d.getRange('E1:H450').format.columnWidth=16;
d.getRange(`E2:H${rows.length+1}`).setNumberFormat('#,##0');d.freezePanes.freezeRows(1);
const n=rows.length+1;
s.getRange('B2').values=[['Hotel bookings | arrival-date report']];s.getRange('B2').format.font={size:15,bold:true};
s.getRange('B4').values=[['Arrival year']];s.getRange('C4').values=[[2016]];s.getRange('C4').dataValidation={rule:{type:'list',values:['2015','2016','2017']}};
s.getRange('E4').values=[['Hotel']];s.getRange('F4').values=[['City Hotel']];s.getRange('F4').dataValidation={rule:{type:'list',values:['City Hotel','Resort Hotel']}};
s.getRange('C4').format.fill='#FFF0BA';s.getRange('F4').format.fill='#FFF0BA';
s.getRange('B6:F6').values=[['Bookings','Canceled flag','Cancellation rate','Checked out','No shows']];
s.getRange('B6:F6').format={fill:'#263D5B',font:{bold:true,color:'#FFFFFF'}};
const sum=(col)=>`SUMIFS('Monthly source'!$${col}$2:$${col}$${n},'Monthly source'!$A$2:$A$${n},$C$4,'Monthly source'!$C$2:$C$${n},$F$4)`;
s.getRange('B7:F7').formulas=[[`=${sum('E')}`,`=${sum('F')}`,'=IF(B7=0,"n.a.",C7/B7)',`=${sum('G')}`,`=${sum('H')}`]];
s.getRange('B7:F7').format.font={size:14,bold:true};s.getRange('B7:F7').setNumberFormat('#,##0');s.getRange('D7').setNumberFormat('0.0%');
s.getRange('B9').values=[['2015 covers July-Dec; 2017 covers Jan-Aug. Compare matching months.']];s.getRange('B9').format.font={italic:true,size:10,color:'#596579'};
s.getRange('B11:F11').values=[['Arrival month','Bookings','Canceled flag','Cancellation rate','Coverage']];
s.getRange('B11:F11').format={fill:'#263D5B',font:{bold:true,color:'#FFFFFF'}};
for(let m=1;m<=12;m++){
 const r=m+11;const mm=String(m).padStart(2,'0');
 s.getRange(`B${r}`).values=[[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]]];
 const count=`COUNTIFS('Monthly source'!$B$2:$B$${n},$C$4&"-${mm}",'Monthly source'!$C$2:$C$${n},$F$4)`;
 const agg=col=>`SUMIFS('Monthly source'!$${col}$2:$${col}$${n},'Monthly source'!$B$2:$B$${n},$C$4&"-${mm}",'Monthly source'!$C$2:$C$${n},$F$4)`;
 s.getRange(`C${r}:F${r}`).formulas=[[`=IF(${count}=0,"n.a.",${agg('E')})`,`=IF(${count}=0,"n.a.",${agg('F')})`,`=IF(ISNUMBER(C${r}),D${r}/C${r},"n.a.")`,`=IF(${count}=0,"Outside snapshot","Observed")`]];
}
s.getRange('C12:D23').setNumberFormat('#,##0');s.getRange('E12:E23').setNumberFormat('0.0%');
s.getRange('B26:F26').values=[['Channel','Bookings','Canceled flag','Cancellation rate','Share of bookings']];
s.getRange('B26:F26').format={fill:'#263D5B',font:{bold:true,color:'#FFFFFF'}};
const channels=[...new Set(rows.map(r=>r[3]))].sort();
channels.forEach((channel,i)=>{const r=i+27;s.getRange(`B${r}`).values=[[channel]];const agg=col=>`${sum(col).slice(0,-1)},'Monthly source'!$D$2:$D$${n},B${r})`;s.getRange(`C${r}:F${r}`).formulas=[[`=${agg('E')}`,`=${agg('F')}`,`=IF(C${r}=0,"n.a.",D${r}/C${r})`,`=IF($B$7=0,"n.a.",C${r}/$B$7)`]];});
s.getRange('C27:D31').setNumberFormat('#,##0');s.getRange('E27:F31').setNumberFormat('0.0%');
s.getRange('B34').values=[['Channel bookings vs report total']];s.getRange('E34').formulas=[['=SUM(C27:C31)-B7']];
s.getRange('B35').values=[['Channel cancellations vs report total']];s.getRange('E35').formulas=[['=SUM(D27:D31)-C7']];
s.getRange('B37').values=[['Canceled flag includes no-shows. Checked out uses the explicit reservation status.']];
s.getRange('B38').values=[['Amber cells are editable filters; source rows are complete monthly aggregates.']];
s.getRange('B39').values=[['Reconciliation differences above should be zero. No occupancy or revenue estimate is made.']];
s.getRange('B1:B40').format.columnWidth=22;s.getRange('C1:F40').format.columnWidth=19;s.getRange('F1:F40').format.columnWidth=22;
const chart=s.charts.add('line',[s.getRange('B11:B23'),s.getRange('C11:C23')]);chart.title='Bookings by arrival month';chart.setPosition('H11','O26');chart.hasLegend=false;
chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:10}};chart.yAxis={numberFormatCode:'#,##0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial'}};chart.series.items[0].line={fill:'#326D9C',style:'solid',width:2};chart.titleTextStyle.fontSize=12;
const notes=[['Metric','Definition'],['Source','Onyx Data July 2023 hotel workbook; hotel_bookings sheet.'],['Original study','Antonio, de Almeida & Nunes (2019), Hotel booking demand datasets.'],['Citation','https://doi.org/10.1016/j.dib.2018.11.126'],['Source unit','One row per historical booking; not a unique guest.'],['Report grain','All source bookings aggregated by arrival month, hotel and channel.'],['Bookings','Sum of booking counts for the selected arrival year and hotel.'],['Canceled flag','Sum of is_canceled, including No-Show records.'],['Checked out','Count of reservation_status equal to Check-Out.'],['Rate','Canceled flag / bookings, calculated from counts, not averaged rates.'],['Coverage','Jul 2015 to Aug 2017; partial years must not be directly compared.'],['Unknown channel','The original Undefined label remains distinct; no invented mapping.'],['Source rows',metrics.bookings],['Source cancellations',metrics.canceled],['Formula check','Report E34 and E35 reconcile channel details to the selected totals.'],['Power Query','Companion .pq script is supplied separately; not embedded or executed here.'],['PivotTables','Pivot setup instructions supplied; no native PivotTable is embedded.'],['Power BI','Original PBIX preserved; not reopened or refreshed in Power BI Desktop.']];
l.getRange(`A1:B${notes.length}`).values=notes;l.getRange('A1:B1').format={fill:'#263D5B',font:{bold:true,color:'#FFFFFF'}};l.getRange('A1:A25').format.columnWidth=24;l.getRange('B1:B25').format.columnWidth=100;l.freezePanes.freezeRows(1);
wb.recalculate();
const checks=[];
for(const year of [2015,2016,2017])for(const hotel of ['City Hotel','Resort Hotel']){
 s.getRange('C4').values=[[year]];s.getRange('F4').values=[[hotel]];wb.recalculate();
 const expected=rows.filter(r=>r[0]===year&&r[2]===hotel).reduce((a,r)=>[a[0]+r[4],a[1]+r[5],a[2]+r[6],a[3]+r[7]],[0,0,0,0]);
 const actual=s.getRange('B7:F7').values[0];if(actual[0]!==expected[0]||actual[1]!==expected[1]||actual[3]!==expected[2]||actual[4]!==expected[3])throw Error(JSON.stringify({year,hotel,actual,expected}));
 checks.push({year,hotel,bookings:actual[0],canceled:actual[1],channel_differences:s.getRange('E34:E35').values});
}
s.getRange('C4').values=[[2016]];s.getRange('F4').values=[['City Hotel']];wb.recalculate();
await fs.writeFile(root+'excel/validation.json',JSON.stringify(checks,null,2));
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'Formula scan'})).ndjson);
for(const [sheetName,range,file] of [['Report','B2:O39','excel/report-preview.png'],['Monthly source','A1:H15','excel/source-preview.png'],['Definitions','A1:B18','excel/definitions-preview.png']]){
 const preview=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(root+file,new Uint8Array(await preview.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(root+'excel/Hotel Reporting.xlsx');
console.log('Saved verified Excel report',checks);
