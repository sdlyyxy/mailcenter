

import urllib2,os,re,urllib,time
from lxml import etree

def gethtml(r):
    attempts = 0
    success = False
    res=''
    while attempts < 5 and not success:
        time.sleep(0.5)
        try:
            res=urllib2.urlopen(r,timeout=5).read()
            success = True
        except:
            attempts += 1
    return res


index='http://epaper.qlwb.com.cn/qlwb/content/'
header='Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
request = urllib2.Request(index)
request.add_header('User-Agent', header)
# html = urllib2.urlopen(request,timeout=5).read()
html=gethtml(request)
if html=='':
    print("get 'http://epaper.qlwb.com.cn/qlwb/content/' error!!!!!!!!!")
    exit()
pattern=re.compile(r'<A HREF="/qlwb/content/(........)/">........</A><br>')#why received html label is uppercase?
alldates=pattern.findall(html)
lastdate=len(alldates)-1 # An integer
_date=alldates[lastdate]
d_request = urllib2.Request(index+_date)
d_request.add_header('User-Agent', header)
d_html = urllib2.urlopen(d_request).read()
d_pattern=re.compile(r'/qlwb/content/(......../ArticelA........htm)')#article articel?
d_match=d_pattern.findall(d_html)
# d_pages=len(d_match)
finalhtml='''
<meta charset="utf8">
<style>
.fbt{
    text-align: center;
    font-size: 30px;
}
.zb{
    text-align: center;
    font-size: 40px;
}
.newspic{
    text-align: center;
}
.FloatTitle{
    text-align:center;
    display:block;
    font-size:28px;
    padding-top:30px;
}
#contenttext div{
    text-align: center;
    font-size: 20px;
}
#contenttext {
    font-size: 24px;
}
#contenttext img{
    width:95%;
    height:auto;
}
</style>
'''
for s in d_match:
    s_request=urllib2.Request(index+s)
    s_request.add_header('User-Agent',header)
    # s_html=urllib2.urlopen(s_request).read()
    s_html=gethtml(s_request)
    if s_html=='':
        print("get single page %s error!!!!!!!!!",index+s)
        exit()
    # s_pattern=re.compile(r'(<div class="fbt">.*<div class="fbt">.*</div>)')
    # s_match=s_pattern.findall(s_html)
    # for item in s_match:
    #     finalhtml=finalhtml+item
    # s_pattern=re.compile(r'(<span id="contenttext">.*</span>)')
    # s_match=s_pattern.findall(s_html)
    # for item in s_match:
    tree=etree.HTML(s_html)
    fbts = tree.xpath("//div[@class='fbt']")
    zbts=tree.xpath("//div[@class='zb']")
    content=tree.xpath("//span[@id='contenttext']")
    finalhtml=finalhtml+etree.tostring(fbts[0])+etree.tostring(zbts[0])+etree.tostring(fbts[1])\
        +etree.tostring(content[0]).replace('../../','http://epaper.qlwb.com.cn/qlwb/')+'<hr>'
    # finalhtml=finalhtml+item.replace('../../','http://epaper.qlwb.com.cn/qlwb/')

print(finalhtml)

