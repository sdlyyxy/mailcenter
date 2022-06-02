import userids
import datetime
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed
from weibo_api.client import WeiboClient
# import pdb
datedelta=datetime.timedelta(days=1)
today=(datetime.datetime.now()-datedelta).date()

def safelyGetText(status):
    mainContent=""
    try:
        mainContent=status.longTextContent
    except:
        try:
            mainContent=status.text
        except:
            mainContent="Text content of this Weibo cannot be fetched.\n"
            # pdb.set_trace()
    return mainContent

@retry(stop=stop_after_attempt(20),wait=wait_fixed(200))
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
        res=res+'<a href="https://m.weibo.cn/u/%s">%s</a>'%(userid,p.name)
        res=res+u"：{}".format(safelyGetText(status))+"</br>"
        for url in status.pic_urls:
            res+='<img src="%s" alt="Weibo Image Cannot be loaded..."></br></br>'%url
            # res+='<div style="width:240"><img src="%s" alt="Weibo Image Cannot be loaded..." style="width:100%%;height:auto"></div></br></br>'%url
        if status.retweeted_status:
            try:
                cl = WeiboClient() 
                pp = cl.status(status.retweeted_status.get("id"))
                res=res+'<a href="https://m.weibo.cn/detail/%s">原推：%s：</a>%s</br>'%(status.retweeted_status.get("id"),status.retweeted_status.get("user").get("screen_name"),safelyGetText(pp))
                for pic in status.retweeted_status.get('pics', []):
                    res+='<img src="%s" alt="Weibo Image Cannot be loaded..."></br></br>'%(pic.get('url'))
            except:
                res+="原推获取异常</br>"
        # 原推可能出现的问题：抱歉，由于作者设置，你暂时没有这条微博的查看权限哦。查看帮助： 网页链接，导致：
        #   File "/home/bupt/projects/mailcenter/get_weibo.py", line 46, in getWeiboByID
        # res=res+'<a href="https://m.weibo.cn/detail/%s">原推：%s：</a>%s</br>'%(status.retweeted_status.get("id"),status.retweeted_status.get("user").get("screen_name"),safelyGetText(p))
        # AttributeError: 'NoneType' object has no attribute 'get'
        try:
            res+="转发：%s  评论：%s 点赞：%s</br>"%(status.reposts_count,status.comments_count,status.attitudes_count)
        except:
            res+="这条微博无法抓取，请手动查看。</br>"
        res=res+"</br></br></br>"
    res+="</br></br></br>"

    return res

res=""
for id in userids.userids:
    res+=getWeiboByID(id)

