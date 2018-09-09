'school news/information collection'

import urllib.request
import json
import datetime
import time
import re


'todo: change day delta(4 places)'

url = 'https://webapp.bupt.edu.cn/extensions/wap/news/get-list.html?p=%s&type=tzgg'

ress = "<h2>"+ (datetime.datetime.now() -
                   datetime.timedelta(days=1)).strftime('%Y年%m月%d日')+"通知公告</h2>\n</br>"

def getInform(i):    
    ress=''
    _url = url % i
    if i==1:
        _url='https://webapp.bupt.edu.cn/extensions/wap/news/list.html?type=tzgg'
    # print(_url)
    datepattern = (datetime.datetime.now() -
                   datetime.timedelta(days=1)).strftime('%Y年%m月%d日')
    # print(datepattern)
    response = urllib.request.urlopen(_url)
    s = str(response.read(), encoding="utf8")
    if i==1:
        res_tr = r'<body >(.*?)</body>'
        m_tr =  re.findall(res_tr,s,re.S|re.M)
        ress=m_tr[0]
        # print(ress)
        ress=ress.replace('/extensions/wap/news/detail.html','https://webapp.bupt.edu.cn//extensions/wap/news/detail.html')
        # print(ress)
        return ress
    data = json.loads(s)
    # print(data['data'].keys())
    if datepattern in data['data'].keys():
        # print('heh')
        for i in data['data'][datepattern]:
            ress+="<meta charset='utf8'><a href='%s'>%s</a></br>\n%s\n</br></br>"%('https://webapp.bupt.edu.cn/extensions/wap/news/detail?id=%s&classify_id=tzgg'%(i['id']),i['title'],i['desc'])
            # print(ress)
    return ress
    
def getNews(i):
    ress=''
    _url = "https://webapp.bupt.edu.cn/extensions/wap/news/get-list.html?p=%s&type=0" % i
    datepattern = (datetime.datetime.now() -
                   datetime.timedelta(days=1)).strftime('%Y年%m月%d日')
    # print(datepattern)
    response = urllib.request.urlopen(_url)
    s = str(response.read(), encoding="utf8")
    data = json.loads(s)
    # print(data['data'].keys())
    if datepattern in data['data'].keys():
        # print('heh')
        for i in data['data'][datepattern]:
            ress+="<meta charset='utf8'><a href='%s'>%s</a></br>\n%s\n</br></br>"%('https://webapp.bupt.edu.cn/extensions/wap/news/detail?id=%s&classify_id=xnxw'%(i['id']),i['title'],i['desc'])
            # print(ress)
    return ress


for i in range(1,4+1):
    ress+=getInform(i)

ress+="<h2>"+ (datetime.datetime.now() -
                   datetime.timedelta(days=1)).strftime('%Y年%m月%d日')+"校园新闻</h2>\n</br>"

for i in range(1,8+1):
    ress+=getNews(i)
