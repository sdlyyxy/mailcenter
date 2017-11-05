import get_basketball
import school_collect
import send_html_mail

send_html_mail.send(get_basketball.today+" 篮球动态",get_basketball.mailcontent)

send_html_mail.send(get_basketball.today+' 伟大北邮新建设',school_collect.ress)