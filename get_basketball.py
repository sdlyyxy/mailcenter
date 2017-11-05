import sqlite3,urllib.request,json,datetime,time,password_ini

# todO:uncomment cba data collect

dbroot=password_ini.dbroot
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
    # print(i)
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

datedelta=datetime.timedelta(days=1)
today=(datetime.datetime.now()-datedelta).strftime("%Y-%m-%d")


response = urllib.request.urlopen(
    "http://api.suredbits.com/nba/v0/games/"+urlDayStr)
s = str(response.read(), encoding="utf8")
data = json.loads(s)

mailcontent='<meta charset="utf8">'

mailcontent += '<h2>%s NBA 比赛结果</h2>\n'%today
for i in data:
    if not i['finished']:
        continue
    # mailcontent = mailcontent + teamIDConvert(i['homeTeam']['teamID']) + ' ' + "%s" % i['homeTeam']['finalScore']\
    #     + '  :  ' + "%s" % i['awayTeam']['finalScore'] + \
    #     ' ' + teamIDConvert(i['awayTeam']['teamID']) + '\n'
    mailcontent+='%s|%s %s:%s<br>\n'%(teamIDConvert(i['homeTeam']['teamID']),teamIDConvert(i['awayTeam']['teamID']),i['homeTeam']['finalScore'],i['awayTeam']['finalScore'])

# print(mailcontent)

mailcontent+='\n\n'

mailcontent+="<h2>%s CBA 比赛结果</h2>\n"%today
conn=sqlite3.connect(dbroot+'cba.db')
c=conn.cursor()
res=c.execute('select * from matches where date="%s"'%today)
for i in res:
    mailcontent+='%s|%s %s:%s<br>\n'%(i[0],i[1],i[2],i[3])

mailcontent+='\n'

response = urllib.request.urlopen(
    "http://china.nba.com/static/data/season/conferencestanding.json")
s = str(response.read(), encoding="utf8")
data = json.loads(s)
data=data['payload']['standingGroups']
teams=[]
for i in data[0]['teams']:
    teams+=[[i['profile']['name'],i['standings']['confRank'],i['standings']['wins'],i['standings']['losses'],i['standings']['streak'][2:]+'连'+i['standings']['streak'][0]]]
teams.sort(key=lambda x:x[1])
mailcontent+="<h2>"+datetime.datetime.now().strftime('%Y/%m/%d %H:%M ')+'NBA联盟排名</h2>\n'
mailcontent+='<h4>东部排名</h4><table>\n'
for i in teams:
    # if(i[0]=='凯尔特人'):
    #     tmp="%s\t%s%s\t%s\t%s\n"%(i[1],i[0],i[2],i[3],i[4])
    #     mailcontent+=tmp
    #     # print()
    #     continue
    
    tmp="<tr><td>%s</td><td>%s</td><td>%s胜</td><td>%s负</td><td>%s</td></tr>"%(i[1],i[0],i[2],i[3],i[4])
    mailcontent+=tmp
    # print(tmp)

teams=[]
for i in data[1]['teams']:
    teams+=[[i['profile']['name'],i['standings']['confRank'],i['standings']['wins'],i['standings']['losses'],i['standings']['streak'][2:]+'连'+i['standings']['streak'][0]]]
teams.sort(key=lambda x:x[1])
mailcontent+='\n</table><h4>西部排名</h4><table>\n'
for i in teams:
    tmp="<tr><td>%s</td><td>%s</td><td>%s胜</td><td>%s负</td><td>%s</td></tr>"%(i[1],i[0],i[2],i[3],i[4])
    mailcontent+=tmp
    # print(tmp)

mailcontent+='</table>'

mailcontent+="<h2>"+datetime.datetime.now().strftime('%Y/%m/%d %H:%M ')+'CBA联盟排名</h2><table>\n'
response = urllib.request.urlopen(
    "https://api-cba.9h-sports.com/api/League/GetRankList/2")
s = str(response.read(), encoding="utf8")
data = json.loads(s)
for i in data['data']:
    tmp="<tr><td>%s</td><td>%s</td><td>%s胜</td><td>%s负</td></tr>"%(i['order'],i['name'],i['wins'],i['loses'])
    mailcontent+=tmp

mailcontent+='</table>'

response = urllib.request.urlopen(
    "https://stats.nba.com/js/data/widgets/home_season.json")
s = str(response.read(), encoding="utf8")
data = json.loads(s)
mailcontent+='<h3>NBA 得分榜</h3><table>'
for i in data['items'][0]['items'][0]['playerstats']:
    mailcontent+='<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(i['PLAYER_NAME'],i['TEAM_ABBREVIATION'],i['PTS'])
mailcontent+='</table>'

mailcontent+='<h3>NBA 篮板榜</h3>'

mailcontent+='<table>'
for i in data['items'][0]['items'][1]['playerstats']:
    mailcontent+='<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(i['PLAYER_NAME'],i['TEAM_ABBREVIATION'],i['REB'])
mailcontent+='</table>'



mailcontent+='<h3>NBA 助攻榜</h3>'
mailcontent+='<table>'
for i in data['items'][0]['items'][2]['playerstats']:
    mailcontent+='<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(i['PLAYER_NAME'],i['TEAM_ABBREVIATION'],i['AST'])
mailcontent+='</table>'


mailcontent+='<h3>NBA 盖帽榜</h3>'
mailcontent+='<table>'
for i in data['items'][0]['items'][3]['playerstats']:
    mailcontent+='<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(i['PLAYER_NAME'],i['TEAM_ABBREVIATION'],i['BLK'])
mailcontent+='</table>'


mailcontent+='<h3>NBA 抢断榜</h3>'
mailcontent+='<table>'
for i in data['items'][0]['items'][4]['playerstats']:
    mailcontent+='<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(i['PLAYER_NAME'],i['TEAM_ABBREVIATION'],i['STL'])
mailcontent+='</table>'


# print(mailcontent)
