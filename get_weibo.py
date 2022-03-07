import userids
import datetime
from weibo_api.client import WeiboClient

datedelta=datetime.timedelta(days=1)
today=(datetime.datetime.now()-datedelta).date()


def getWeiboByID(userid):
    client = WeiboClient() 
    res=""
    p = client.people(userid)  # 用户ID，后期加可以根据昵称创建用户
    res=res+u"用户名：{}".format(p.name)+"</br>"
    res=res+u"用户简介：{}".format(p.description)+"</br>"
    res=res+u'用户链接：<a href="https://m.weibo.cn/u/%s">https://m.weibo.cn/u/%s</a>'%(userid,userid)+"</br>"
    res=res+u"Ta关注的用户数：{}".format(p.follow_count)+"</br>"
    res=res+u"关注Ta的用户数：{}".format(p.followers_count)+"</br></br>"
    res=res+u"Ta最近发布的："+"</br>"
    res=res+"</br>"
    for status in p.statuses.page(1):    
        dt = datetime.datetime.strptime(status.created_at, "%a %b %d %H:%M:%S %z %Y")
        if dt.date()>today:
            continue
        if dt.date()<today:
            break
        res=res+u'<a href="https://m.weibo.cn/detail/%s">https://m.weibo.cn/detail/%s</a>'%(status.id,status.id)+"</br>"
        res=res+u"发布时间：{}".format(dt.strftime("%Y年%m月%d日 %H:%M:%S"))+"</br>"
        res=res+u"正文内容：{}".format(status.longTextContent)+"</br>"
        for url in status.pic_urls:
            res+='<img src="%s" alt="Weibo Image Cannot be loaded..."></br></br>'%url
            # res+='<div style="width:240"><img src="%s" alt="Weibo Image Cannot be loaded..." style="width:100%%;height:auto"></div></br></br>'%url
        if status.retweeted_status:
            cl = WeiboClient() 
            p = cl.status(status.retweeted_status.get("id"))
            res=res+'<a href="https://m.weibo.cn/detail/%s">原推：%s：</a>%s</br>'%(status.retweeted_status.get("id"),status.retweeted_status.get("user").get("screen_name"),p.longTextContent)
            for pic in status.retweeted_status.get('pics', []):
                res+='<img src="%s" alt="Weibo Image Cannot be loaded..."></br></br>'%(pic.get('url'))

        res+="转发：%s  评论：%s 点赞：%s</br>"%(status.reposts_count,status.comments_count,status.attitudes_count)
        res=res+"</br></br></br>"
    res+="</br></br></br>"

    return res

res=""
for id in userids.userids:
    res+=getWeiboByID(id)

