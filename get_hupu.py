import urllib
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed
from urllib.request import urlopen
import json


@retry(stop=stop_after_attempt(7),wait=wait_fixed(2))
def urlopen_with_retry(urlstr):
    return urlopen(urlstr)


res=""

url = "https://m.hupu.com/api/v2/home-feed/%d"
  
for i in range(1,3+1):
    response = urlopen_with_retry(url%i)
    data_json = json.loads(response.read())
    for j in data_json["data"]["list"]:
        res+='%s：<a href="%s">链接</a></br></br>'%(j["title"],j["url"])

