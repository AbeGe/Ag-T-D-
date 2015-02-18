import urllib.parse 
import urllib.request
import re
from bs4 import BeautifulSoup
import datetime
import time

def GetData(fo,md,soup):
    text = [ [md] + [tCol.get_text() for tCol in tRow.find_all('td')] for tRow in soup.find_all('tr')]
    content = '\n'.join([''.join(['{:16}'.format(col) for col in row]) for row in text if row[1].startswith('Ag(T+D')])
    fo.write('\n')
    fo.write(content)
#=============End function============

preUrl = 'http://www.sge.com.cn/xqzx/mrxq/'
fo = open('AgData.txt','w',encoding='utf-8')
for i in range(1,10,1):
	page = urllib.request.urlopen(preUrl + 'index' + ("_"+str(i) if i>1 else "") + '.shtml').read().decode('UTF8')
	#'http://www.sge.com.cn/xqzx/mrxq/524349.shtml'.read()
	subIndex = re.findall('href="/xqzx/mrxq/(\d+\.shtml)"',page)
	for tIndex in subIndex:
		subPage = urllib.request.urlopen('http://www.sge.com.cn/xqzx/mrxq/' + tIndex).read().decode()
		soup = BeautifulSoup(subPage)
		md = re.findall('\d{4}-\d{2}-\d{2}',soup.find(class_="tit_bottom").text)
		print(md,end='\n\n')
		GetData(fo,md,soup)
fo.close()
print('end')
