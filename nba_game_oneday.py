import sqlite3,urllib.request,json,datetime,time

dbroot='/root/project/mailcenter'
def process(url):
    response=urllib.request.urlopen(url)
    s = str(response.read(), encoding="utf8")
    data = json.loads(s)
    for i in data['data']:
        if i['league_match']['matchStatus']==1:
            tmp=i['league_match']
            datestr=time.strftime("%Y-%m-%d",time.localtime(tmp['matchTime']/1000))
            conn = sqlite3.connect(dbroot+'cba.db')
            c = conn.cursor()
            cursor=c.execute('delete from matches where id=%s'%tmp['id'])
            c.execute('''insert into matches values ('%s','%s',%s,%s,'%s',%s)
            '''%(tmp['home_club_abbr'],tmp['guest_club_abbr'],tmp['homeScore'],\
            tmp['guestScore'],datestr,tmp['id']))
            conn.commit()
            conn.close()
    
for i in range(1,38+1):
    print(i)
    url='https://api-cba.9h-sports.com/api/League/GetMatchCurrent?year=20172018&round=%s'%i
    process(url)

def teamIDConvert(name):
    dic = {'ATL': '老鹰', 'MIA': '热火', 'BKN': '篮网', 'MIL': '雄鹿',
           'BOS':	'凯尔特人', 	'MIN': 	'森林狼',
           'CHA': 	'黄蜂', 'NOP':	"鹈鹕",
           'CHI':	'公牛', 	'NYK': 	 '尼克斯',
           'CLE': 	'骑士', 	'OKC':	'雷霆',
           'DAL':	'小牛',	'ORL':	'魔术',
           'DEN':	'掘金',	'PHI':	'76人',
           'DET':	'活塞',	'PHX':	'太阳',
           'GSW':	'勇士',	'POR':	'开拓者',
           'HOU':	'火箭',	'SAC':	'国王',
           'IND':	'步行者', 	'SAS':	'马刺',
           'LAC':	'快船',	'TOR':	'猛龙',
           'LAL':	'湖人',	'UTA':	'爵士',
           'MEM': 	'灰熊',	'WAS':	'奇才'
           }
    return dic[name]






import time,datetime

delta=datetime.timedelta(days=2)
nbaday=datetime.datetime.now()-delta
urlDayStr=nbaday.strftime("%Y/%m/%d")

import urllib.request
import json,sqlite3
response = urllib.request.urlopen(
    "http://api.suredbits.com/nba/v0/games/"+urlDayStr)
s = str(response.read(), encoding="utf8")
data = json.loads(s)

mailcontent = '%s NBA 比赛结果\n'%urlDayStr
for i in data:
    if not i['finished']:
        continue
    # mailcontent = mailcontent + teamIDConvert(i['homeTeam']['teamID']) + ' ' + "%s" % i['homeTeam']['finalScore']\
    #     + '  :  ' + "%s" % i['awayTeam']['finalScore'] + \
    #     ' ' + teamIDConvert(i['awayTeam']['teamID']) + '\n'
    mailcontent+='%s|%s %s:%s\n'%(teamIDConvert(i['homeTeam']['teamID']),teamIDConvert(i['awayTeam']['teamID']),i['homeTeam']['finalScore'],i['awayTeam']['finalScore'])

# print(mailcontent)

mailcontent+='\n\n'


httpheader = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
# req=urllib.request.Request(url,headers=httpheader)
response = urllib.request.urlopen(
    "http://china.nba.com/static/data/season/conferencestanding.json")
s = str(response.read(), encoding="utf8")
data = json.loads(s)
data=data['payload']['standingGroups']
teams=[]
for i in data[0]['teams']:
    teams+=[[i['profile']['name'],i['standings']['confRank'],i['standings']['wins'],i['standings']['losses'],i['standings']['streak'][2:]+'连'+i['standings']['streak'][0]]]
teams.sort(key=lambda x:x[1])
mailcontent+=datetime.datetime.now().strftime('%Y/%m/%d')+'联盟排名\n'
mailcontent+='东部排名\n'
for i in teams:
    if(i[0]=='凯尔特人'):
        tmp="%s\t%s%s\t%s\t%s\n"%(i[1],i[0],i[2],i[3],i[4])
        mailcontent+=tmp
        # print()
        continue
    
    tmp="%s\t%s\t%s\t%s\t%s\n"%(i[1],i[0],i[2],i[3],i[4])
    mailcontent+=tmp
    # print(tmp)

teams=[]
for i in data[1]['teams']:
    teams+=[[i['profile']['name'],i['standings']['confRank'],i['standings']['wins'],i['standings']['losses'],i['standings']['streak'][2:]+'连'+i['standings']['streak'][0]]]
teams.sort(key=lambda x:x[1])
mailcontent+='\n西部排名\n'
for i in teams:
    if(i[0]=='凯尔特人'):
        tmp="%s\t%s%s\t%s\t%s\n"%(i[1],i[0],i[2],i[3],i[4])
        mailcontent+=tmp
        # print()
        continue
    
    tmp="%s\t%s\t%s\t%s\t%s\n"%(i[1],i[0],i[2],i[3],i[4])
    mailcontent+=tmp
    # print(tmp)

datedelta=datetime.timedelta(days=1)
today=(datetime.datetime.now()-datedelta).strftime("%Y-%m-%d")
mailcontent+="\n\n%s CBA 比赛结果\n"%today
conn=sqlite3.connect(dbroot+'cba.db')
c=conn.cursor()
res=c.execute('select * from matches where date="%s"'%today)
for i in res:
    mailcontent+='%s|%s %s:%s\n'%(i[0],i[1],i[2],i[3])

print(mailcontent)

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# from_addr = input('From: ')
# password = input('Password: ')
# to_addr = input('To: ')
# smtp_server = input('SMTP server: ')

from_addr = 'qq827062223@me.com'
# from_addr = input('From: ')
password = 'kcow-twvw-wwsf-vwme'
# 输入收件人地址:
to_addr = 'sdlyyxy@icloud.com'
# 输入SMTP服务器地址:
smtp_server = 'smtp.mail.me.com'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
# from_addr = 'yxy9851@sina.com'
# # from_addr = input('From: ')

# # 输入收件人地址:
# to_addr = 'sdlyyxy@me.com'
# # 输入SMTP服务器地址:
# smtp_server = 'smtp.sina.com'


msg = MIMEText(mailcontent, 'plain', 'utf-8')
msg['From'] = _format_addr('sdlyyxy <%s>' % from_addr)
msg['To'] = _format_addr('sdlyyxy <%s>' % to_addr)
msg['Subject'] = Header('%s 赛事动态'%today, 'utf-8').encode()

# server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
