import urllib.parse
import urllib.request
import re
import json

myUrl = 'http://www.sge.com.cn/sgeclient/sgeData/public/json/delaydata.json'
content = urllib.request.urlopen(myUrl).read().decode()
obj=json.loads(content)
print(obj[0]["VRT_CODE"] + obj[0]["DELAY_TIME"])
print('current:' + obj[0]['LAST_PRICE'])
print('low    :' + obj[0]['LOW_PRICE'])
print('High   :'+ obj[0]['HIGH_PRICE'])
print("============================================")
t=input()
