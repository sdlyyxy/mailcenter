import sqlite3,urllib.request,json,datetime,time

def process(url):
    response=urllib.request.urlopen(url)
    s = str(response.read(), encoding="utf8")
    data = json.loads(s)
    for i in data['data']:
        if i['league_match']['matchStatus']==1:
            tmp=i['league_match']
            datestr=time.strftime("%Y-%m-%d",time.localtime(tmp['matchTime']/1000))
            conn = sqlite3.connect('cba.db')
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