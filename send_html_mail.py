from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import password_ini
import to_addrs


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# server = smtplib.SMTP(smtp_server, 25)

def send(subject,content,ishtml):
    from_addr = 'qq827062223@me.com'
    # from_addr='827062223@qq.com'
    # from_addr='sdlyyxy@sina.com'
    password = password_ini.mailpassword
    smtp_server = 'smtp.mail.me.com'
    # smtp_server='smtp.qq.com'
    # smtp_server='smtp.sina.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    content+='''
    <br><br><br><br><hr>Proudly presented by <a href="mailto:sdlyyxy@icloud.com">sdlyyxy（燕新宇）</a>, project <a href='https://github.com/sdlyyxy/mailcenter'>mailcenter</a>.
    '''
    if ishtml:
        msg = MIMEText(content, 'html', 'utf-8')    
    else:
        msg = MIMEText(content, 'plain', 'utf-8')  
    msg['From'] = _format_addr('mailcenter <%s>' % from_addr)
    msg['To'] = _format_addr('sdlyyxy <sdlyyxy@icloud.com>')
    msg['Subject'] = Header(subject, 'utf-8').encode()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs.addrs, msg.as_string())
    server.quit()
