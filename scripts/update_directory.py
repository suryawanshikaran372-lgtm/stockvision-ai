#!/usr/bin/env python3
"""Refresh public symbol directories; keep last successful snapshot if upstream fails."""
import csv, io, json, pathlib, urllib.request, datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEST=ROOT/'data/companies.json'
HEADERS={'User-Agent':'StockVisionAI/2.0 (public research directory; contact via repository)','Accept':'text/plain,text/csv,*/*'}
def download(url):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=25) as resp:return resp.read().decode('utf-8-sig',errors='replace')
def add(store,market,symbol,name,exchange):
    symbol=symbol.strip().upper();name=name.strip()
    if symbol and name and len(symbol)<25 and len(name)<300:store[(market,symbol)]={'market':market,'symbol':symbol,'name':name,'exchange':exchange}
def nasdaq(store):
    t=download('https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt')
    for r in csv.DictReader(io.StringIO(t),delimiter='|'):
        if r.get('Test Issue')=='N' and r.get('ETF')=='N':add(store,'US',r.get('Symbol',''),r.get('Security Name',''),'NASDAQ')
def other(store):
    t=download('https://www.nasdaqtrader.com/dynamic/symdir/otherlisted.txt')
    for r in csv.DictReader(io.StringIO(t),delimiter='|'):
        if r.get('Test Issue')=='N' and r.get('ETF')=='N':add(store,'US',r.get('ACT Symbol') or r.get('NASDAQ Symbol') or '',r.get('Security Name',''),{'N':'NYSE','A':'NYSE American','P':'NYSE Arca','Z':'Cboe'}.get(r.get('Exchange',''),'US exchange'))
def nse(store):
    t=download('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
    for r in csv.DictReader(io.StringIO(t)):
        r={k.strip().upper():v for k,v in r.items() if k}
        if r.get('SERIES','EQ').strip()=='EQ':add(store,'IN',r.get('SYMBOL',''),r.get('NAME OF COMPANY',''),'NSE')
def main():
    old={}
    if DEST.exists():
        try:old={(c['market'],c['symbol']):c for c in json.loads(DEST.read_text()).get('companies',[])}
        except (ValueError,KeyError):pass
    results={}
    for key,fn in [('nasdaq',nasdaq),('other',other),('nse',nse)]:
        subset={}
        try:
            fn(subset)
            if len(subset)<50:raise ValueError('Unexpectedly small response')
            results.update(subset);print(key,len(subset))
        except Exception as exc:
            print('WARNING:',key,str(exc))
            if key=='nse':results.update({k:v for k,v in old.items() if k[0]=='IN'})
            elif key=='nasdaq':results.update({k:v for k,v in old.items() if v.get('exchange')=='NASDAQ'})
            else:results.update({k:v for k,v in old.items() if k[0]=='US' and v.get('exchange')!='NASDAQ'})
    if not results and old:results=old
    if not results:raise SystemExit('No directories available; preserving existing file')
    DEST.parent.mkdir(parents=True,exist_ok=True)
    DEST.write_text(json.dumps({'updated':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'companies':sorted(results.values(),key=lambda c:(c['market'],c['symbol']))},ensure_ascii=False,separators=(',',':'))+'\n')
    print('Total',len(results))
if __name__=='__main__':main()
