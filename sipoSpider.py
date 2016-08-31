#待爬取的URL
#http://cpquery.sipo.gov.cn/txnQueryBibliographicData.do?select-key:shenqingh=2014100055199
#进入实审----     2014100066511     

import re
import requests
import time

class IEspider():
	def getUrl(self,target_url,start_num,end_num):
		url_list=[]
		for i in range(start_num,end_num):
			link=re.sub('shenqingh=','shenqingh=%d' %i,target_url,re.S)
			url_list.append(link)
		return url_list

	def getOkUrl(self,url):
		header={
				'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'zh-CN',
				'Cookie':'bg6149=13|V8Zp6|V8Zcd; _gscu_699342174=72617599l4lk5527; JSESSIONID=f09101f38412ca9d3fb447cdb03a',
				'Host': 'cpquery.sipo.gov.cn',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
				}
		html=requests.get(url,headers=header,timeout=50)
		#案件状态 筛选
		if('进入实审' in html.text):
			#捕获申请号
			shenqingh=re.search('record_zlx:shenqingh" title="(\w{12})\w">',html.text,re.S).group(1)
			return shenqingh
	
	def savePatnum(self,num):
		f=open('OKnum.txt','a')
		f.writelines(num+'\n')
		f.close()
		


if __name__=='__main__':
	
	
	Do=IEspider()
	
	go   = 2014100000000
	stop = 2014200000000
	
	count=go
	all_urls=[]
	origin_url='http://cpquery.sipo.gov.cn/txnQueryBibliographicData.do?select-key:shenqingh='
	
	all_urllist=Do.getUrl(origin_url,go,stop)
	
	for link in all_urllist:
		print(str(count))
		try:
			page=Do.getOkUrl(link)
			pat_num=Do.getOkUrl(link)
			if(pat_num!=None):
				Do.savePatnum(pat_num)
				print('>>>>>>>>>>>>>>符合条件>>>已保存')
			count+=1
			
		except:
			count+=1
			print('超时退出')

	

















	