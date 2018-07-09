import requests
import json

#req = requests.get("https://mirror.fybsg.com/static/trades.json", params={'recent':'10'})
req = requests.get("https://mirror.fybsg.com/api/SGD/trades.json", params={'recent':'10'})
print req.url
#print req.text
trades = req.json()

