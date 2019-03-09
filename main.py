# import get_basketball
import school_collect
import send_html_mail
import datetime
import os

datedelta=datetime.timedelta(days=1)
today=(datetime.datetime.now()-datedelta).strftime("%Y-%m-%d")
paper_today=datetime.datetime.now().strftime("%Y-%m-%d")

os.system('python2 /home/ubuntu/project/mailcenter/qlwb_html.py>/home/ubuntu/project/mailcenter/qlwb.html')
# send_html_mail.send(get_basketball.today+" 篮球动态",get_basketball.mailcontent)
send_html_mail.send(paper_today+" 齐鲁晚报",open('/home/ubuntu/project/mailcenter/qlwb.html').read())

send_html_mail.send(today+' 伟大北邮新建设',school_collect.ress)
