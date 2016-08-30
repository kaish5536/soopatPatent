#coding:utf-8
#作者：王凯盛
#在soopat上查找所有实审，无代理机构，个人申请的发明专利,并抓取相关信息
import requests
import re
import sys
import time
import pool


class spider():
	def getUrl(self,target_url,start_num,end_num):
		url_list=[]
		for i in range(start_num,end_num):
			link=re.sub('Patent/','Patent/%d' %i,target_url,re.S)
			url_list.append(link)
		return url_list
		
	def getHtml(self,link):
		header={
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate, sdch',
				'Accept-Language':'zh-CN,zh;q=0.8',
				'Cache-Control':'max-age=0',
				'Connection':'keep-alive',
				'Cookie':'__utmc=135424883; __utmz=135424883.1472568613.12.11.utmccn=(referral)|utmcsr=www2.soopat.com|utmcct=/Home/Result|utmcmd=referral; advu1=; advu2=; advu3=; advu4=; auth=ec179%2BG4tbM3AggZaA13oA42D6GgzS393TJ%2Bf0jEnRxw5GS2L712hpDy0pbwJrL4P%2F1GgBYD%2FIwjs8eauXhQzl9Ek3g; suid=D8AEFE0DAE523BF1; sunm=kaish; login_credits=1472568754; sid=H3DHsE; patentids=; __utmb=135424883; __utma=135424883.120591016.1461684574.1472558143.1472568613.12',
				'Host':'www2.soopat.com',
				'Upgrade-Insecure-Requests':'1',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
				}
		html=requests.get(link,headers=header,timeout=50)
		
		#页面长度
		#剔除没有该申请号的 状态要求 “审中-”，包括公开和实审，下文二次筛选
		page_content=len(html.text)
		if (page_content>6500 and '审中-' in html.text ):
			#审中状态=实审
			state=re.search('style="cursor:pointer;">审中-(\w{2})</div>',html.text,re.S).group(1)
			#申请人-个人
			proposer=re.search('申请人：</b> <a href=.*?target=_blank>(.*?)</a>',html.text,re.S).group(1)
			#发明人-公告
			inventors=re.search('发明\(设计\)人：</b>(.*?)</td>',html.text,re.S).group(1)
			inventor=re.findall('target=_blank>(.*?)</a>',inventors,re.S)
			#代理-无
			surrogate=re.search('专利代理机构</td>(.*?)</td>',html.text,re.S).group(1)
			
			#实审状态  state=='实审' ,  inventor[0]!='不公告发明人' , geren 申请 len(proposer)<4 ,无代理  len(surrogate)<30      
			
			if(state=='实审' and inventor[0]!='不公告发明人' and len(proposer)<4 and len(surrogate)<50 ):
				info={}
				info['title']=re.search('<h1>(.*?)\r',html.text,re.S).group(1)
				info['num']=re.search('<i>申请号：(.*?) 申请日',html.text,re.S).group(1)
				info['date']=re.search('申请日：(.*?)</i>',html.text,re.S).group(1)
				info['proposer']=proposer
				info['inventor']=inventor
				info['address']=re.search('地址：</b> (.*?)\r',html.text,re.S).group(1)
				info['genre']=re.search('<div  style="font-weight:bold;">(\w).*?</div>',html.text,re.S).group(1)
				
				return info
		elif ('验证码' in html.text):
			return 0

	def saveFile(self,infos):
		f=open('info.txt','a')
		#for each in infos:
		each=infos
		f.writelines('发明名称：'+each['title']+'\n')
		f.writelines('申请号：'+each['num']+'\n')
		f.writelines('申请日期：'+each['date']+'\n')
		f.writelines('申请人：'+each['proposer']+'\n')
		f.writelines('发明人：'+''.join(each['inventor'])+'\n')
		f.writelines('邮编地址：'+each['address']+'\n')
		f.writelines('类别：'+each['genre']+'\n\n')
		
		f.close()
		
if __name__=='__main__':
	
	go   = 201410000593
	stop = 201410005000
	
	count=go
	allinfo=[]
	url='http://www2.soopat.com/Patent/'
	soospider=spider()
	all_urls=soospider.getUrl(url,go,stop)
	
	for link in all_urls:
		print(str(count))
		try:
			page=soospider.getHtml(link)
			if (page!=None and page!=0):
				print('\b'+'>>>>>>符合条件')
				allinfo.append(page)
				#单项保存，避免程序崩溃
				soospider.saveFile(page)
			elif (page==0):
				print('需要输入验证码'+'\n'+'目前已经完成到:'+str(count)+'请稍后继续')
				break
			#print(page)
			count+=1
			time.sleep(2)
		except:
			print('超时跳过')
	print('已存储')
	
	
	

	
	
	
	
	
	
	
	
	
	
	
