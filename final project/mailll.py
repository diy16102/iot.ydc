import poplib
import sys
import smtplib
from email.mime.text import MIMEText
import os
from email.header import decode_header
import email
import time
def check_email():
    try:
        p = poplib.POP3('pop.sina.com')
        p.user('ydc0419@sina.com')
        p.pass_('1d88bc77ae8a54eb')
        ret = p.stat()
    except:
        print('Login failed!')
        sys.exit(1)
    str = p.top(ret[0], 0)
    strlist = []
    for x in str[1]:
            try:
                strlist.append(x.decode())
            except:
                try:
                    strlist.append(x.decode('gbk'))
                except:
                    strlist.append((x.decode('big5')))
    mm = email.message_from_string('\n'.join(strlist))
    sub = decode_header(mm['subject'])
    if sub[0][1]:
        submsg = sub[0][0].decode(sub[0][1])
    else:
        submsg = sub[0][0]
    if submsg.strip() == 'shudown':
        return 0
    elif submsg.strip() == 'restart':
        return 1
    p.quit()
def send_email():
    user = 'ydc0419@sina.com'
    pwd = '1d88bc77ae8a54eb'
    to = ['ydc0419@sina.com', '809518648@qq.com']    
    msg = MIMEText('')
    msg['Subject'] = 'orders reeived!'
    msg['From'] = user
    msg['To'] = ','.join(to)
    s = smtplib.SMTP('smtp.sina.com')
    s.login(user, pwd)
    s.sendmail(user, to, msg.as_string())
    s.close()
 
if __name__ == '__main__':
    while True:
        time.sleep(20)
        if check_email() == 0:
            send_email()
            os.system('shutdown -s -t 1')    
            break
        if check_email() == 1:
            send_email()
            os.system('shutdown -r')      
            break
