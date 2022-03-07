from urllib.request import urlopen
import json

res=""

url = "https://m.hupu.com/api/v2/home-feed/%d"
  
for i in range(1,3+1):
    response = urlopen(url%i)
    data_json = json.loads(response.read())
    for j in data_json["data"]["list"]:
        res+='%s：<a href="%s">链接</a></br></br>'%(j["title"],j["url"])

