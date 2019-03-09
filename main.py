# import get_basketball
import school_collect
import send_html_mail
import datetime
import qlwb_html

datedelta=datetime.timedelta(days=1)
today=(datetime.datetime.now()-datedelta).strftime("%Y-%m-%d")


# send_html_mail.send(get_basketball.today+" 篮球动态",get_basketball.mailcontent)
send_html_mail.send(today+" 齐鲁晚报",qlwb_html.finalhtml)

send_html_mail.send(today+' 伟大北邮新建设',school_collect.ress)