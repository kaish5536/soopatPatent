#在线爬取代理ip#
#coding:utf-8
import os,re,codecs,time
from urllib import request
from bs4 import BeautifulSoup
import encodings

ip_re=r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
port_re=r"<td>(\d{2,4})</td>"
Url='http://www.xicidaili.com/nn'
req=request.Request(Url)
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/44.0.2403.157 UBrowser/5.5.9703.2 Safari/537.36')
htmlDoc = request.urlopen(req).read()
soup = BeautifulSoup(htmlDoc)
print ("正在获取获取ip")
divHtml = soup.find_all("tr")
for link in divHtml:
#    print (link)
    try:
       # print (link)
        ip_number = re.findall(ip_re,str(link))
#        print (ip_number)
        port_number =re.findall(port_re,str(link))
#        print (port_number)
    except:
        print ("失败")
        pass
    finally:
        path='ip'
        if not os.path.exists(path):
            os.makedirs(path)
        if ip_number==[] or port_number==[]:
            pass
        else:
            ip_txt = open('ip.txt','a')
            ip_txt.write("ip="+ip_number[0]+"prot="+port_number[0]+"\n")
            ip_txt.close()
print ("以成功获取ip")

