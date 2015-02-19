#Author:Abe Ge
#Copy right: Gyhan Global Service
#Date: 2015/02/19

import urllib.parse 
import urllib.request
import re
from bs4 import BeautifulSoup
import datetime
import time


# TODO: get_data and get_old_data should be marge to one function. The 'text' adjust should be use a delegate to pass in.
def get_data(fo,md,soup):
    text = [ [md] + [modify_data(tCol.get_text()) for tCol in tRow.find_all('td')] for tRow in soup.find_all('tr')]
    content = '\n'.join(['|'.join([col for col in row]) for row in text if row[1].startswith('Ag(T+D')])
    fo.write('\n')
    fo.write(content)
#=============End function============

def get_old_data(fo,md,soup,direction):
    text = [ [md] + [tCol.get_text() for tCol in tRow.find_all('td')] for tRow in soup.find_all('tr')]
    for row in text:
        row.insert(12,modify_data(direction))
    content = '\n'.join(['|'.join([col for col in row]) for row in text if row[1].startswith('Ag(T+D')])
    fo.write('\n')
    fo.write(content)
#=============End function============

def modify_data(value):
    value = value.replace('\n','').replace('\xa0','').replace('\u3000','')
    value = value.replace('多</','多支付空')
    value = value.replace('多付空','多支付空')
    value = value.replace('<sp','多支付空')
    value = value.replace('空</','空支付多')
    value = value.replace('空 付','空支付多')
    value = value.replace('空付多','空支付多')
    value = value.strip()
    return value
#============End function=============

preUrl = 'http://www.sge.com.cn/xqzx/mrxq/'
fo = open('AgData2.txt','w',encoding='utf-8')
for i in range(1,113,1):  #113
  page = urllib.request.urlopen(preUrl + 'index' + ("_"+str(i) if i>1 else "") + '.shtml').read().decode('UTF8')
  
  #'http://www.sge.com.cn/xqzx/mrxq/524349.shtml'
  subIndex = re.findall('href="/xqzx/mrxq/(\d+\.shtml)"',page)
  for tIndex in subIndex:
    subPage = urllib.request.urlopen('http://www.sge.com.cn/xqzx/mrxq/' + tIndex).read().decode()
    soup = BeautifulSoup(subPage)
    md = re.findall('\d{4}-\d{2}-\d{2}',soup.find(class_="tit_bottom").text)[0]
    direction = re.findall('(?:Ag\(T\+D\)--</b><b>|Ag\(T\+D\)--|Ag\(T\+D\).*?>.*?>.*?>.*?>)(...)',subPage)
    if len(direction)>0:
        direction = direction[0]
    else:
        direction=''
    print(md,end='\n\n')
    if datetime.datetime.strptime(md, '%Y-%m-%d')< datetime.datetime(2014,9,5):
        get_old_data(fo,md,soup,direction)
    else:
        get_data(fo,md,soup)
fo.close()
print('end')

'''
#These code are used for debug
print(modify_data(''))
fo = open('AgData.txt','w',encoding='utf-8')
test = urllib.request.urlopen('http://www.sge.com.cn/xqzx/mrxq/511149.shtml').read().decode()
soup=BeautifulSoup(test)
md = re.findall('\d{4}-\d{2}-\d{2}',soup.find(class_="tit_bottom").text)[0]
if datetime.datetime.strptime(md, '%Y-%m-%d')< datetime.datetime(2014,9,5):
    direction = re.findall('Ag\(T\+D\)--(...)',test)[0]
    get_old_data(fo,md,soup,direction)
fo.close()
'''
