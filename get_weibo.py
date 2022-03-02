import userids

from weibo_api.client import WeiboClient

def getWeiboByID(userid):
    client = WeiboClient() 
    res=""
    p = client.people(userid)  # 用户ID，后期加可以根据昵称创建用户
    res=res+u"用户名：{}".format(p.name)+"\n"
    res=res+u"用户简介：{}".format(p.description)+"\n"
    res=res+u"用户链接：https://m.weibo.cn/u/%s"%userid+"\n"
    res=res+u"Ta关注的用户数：{}".format(p.follow_count)+"\n"
    res=res+u"关注Ta的用户数：{}".format(p.followers_count)+"\n\n"
    res=res+u"Ta最近发布的微博："+"\n"
    res=res+"=================================================="+"\n"
    for status in p.statuses.page(1):    
        res=res+u"发布时间：{}".format(status.created_at)+"\n"
        res=res+u"微博内容概要：{}".format(status.text)+"\n"
        res=res+u"完整链接：https://m.weibo.cn/detail/{}".format(status.id)+"\n"
        res=res+"=================================================="+"\n"
    res+="\n\n\n"
    return res

res=""
for id in userids.userids:
    res+=getWeiboByID(id)

