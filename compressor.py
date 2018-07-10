import requests
import json
import datetime

def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json['date'])
    except KeyError:
        return 0
#,params={'recent':'100'}
req = requests.get("https://mirror.fybsg.com/api/SGD/trades.json")
trades = req.json()

trades.sort(key=extract_time)

compressed = []

date = ''
tHigh = 0
tHighTime = 0
tHighTID = 0

tLow = 100000
tLowTime = 0
tLowTID = 0

tOpen = 0
tOpenTime = 0
tOpenTID = 0

dVol = 0
newDay = True
for trade in trades:
    #print(trade)
    tDate = datetime.datetime.utcfromtimestamp(trade['date']).strftime('%Y-%m-%d')
    if(tDate != date):
        #Save data and reset to new day
        day = {"price":tOpen, "amount":'%.8f' % (dVol/3), "date":tOpenTime, "tid":tOpenTID, "realDay":datetime.datetime.utcfromtimestamp(tOpenTime).strftime('%Y-%m-%d %H-%M')}
        day1 = {"price":tHigh, "amount":'%.8f' % (dVol/3), "date":tHighTime, "tid":tHighTID, "realDay":datetime.datetime.utcfromtimestamp(tHighTime).strftime('%Y-%m-%d %H-%M')}
        day2 = {"price":tLow, "amount":'%.8f' % (dVol/3), "date":tLowTime, "tid":tLowTID, "realDay":datetime.datetime.utcfromtimestamp(tLowTime).strftime('%Y-%m-%d %H-%M')}
        if(date != ''):
            compressed.append(day)
            compressed.append(day1)
            compressed.append(day2)
        #print(day)
        print("%s Volume: %.8f High: %.2f Low %.2f" % (date,dVol, tHigh, tLow))
        date=tDate
        dVol = 0
        tHigh = 0
        tLow = 100000
        newDay = True
    #add volume, find high/low
    if(newDay):
        tOpen = float(trade['price'])
        tOpenTime = int(trade['date'])
        tOpenTID = int(trade['tid'])
        newDay = False
    dVol+= float(trade['amount'])
    if(float(trade['price']) > tHigh):
        tHigh = float(trade['price'])
        tHighTime = int(trade['date'])
        tHighTID = int(trade['tid'])
    if(float(trade['price']) < tLow):
        tLow = float(trade['price'])
        tLowTime = int(trade['date'])
        tLowTID = int(trade['tid'])

finalC = sorted(compressed, key=lambda trade: (trade['date']))
with open("trades.json", "w") as fout:
    print(json.dump(finalC,fout))
