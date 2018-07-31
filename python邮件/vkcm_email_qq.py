#!/usr/bin/python
#coding:utf-8
#yangy114@vanke.com 2018.01.10

import optparse
import os
import smtplib
import sys
import smtplib
import urllib, urllib2
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

def default_email_config_myqq():
    from_addr = '565392985@qq.com'
    displayname = '配置管理'
    password = 'wtbvhlutvteabbbj'
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    transport = "SSL"
    return from_addr, displayname, password, smtp_server, smtp_port, transport

def default_email_config_vanke():
    from_addr = "s-wyrdinfo@vanke.com"
    displayname = 'Vanke CM'
    password = "22hrYQEV"
    smtp_server = "mail.vanke.com"
    smtp_port = 25
    transport = "TLS"
    return from_addr, displayname, password, smtp_server, smtp_port, transport

def send_email(from_addr, displayname, password, to_addr, smtp_server, smtp_port, transport, subject, body, attachment):
    #msg = MIMEMultipart()
    msg = MIMEText(body, _subtype='html', _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = formataddr([displayname, from_addr])
    msg['To'] = ";".join(to_addr)

    # 下面是文字部分，也就是纯文本
    #puretext = MIMEText(body)
    #msg.attach(puretext)

    # 各种附件
    if attachment :
        for i in attachment:
            att_basename = os.path.basename(i)
            attpary = MIMEApplication(open(i, 'rb').read())
            attpary.add_header('Content-Disposition', 'attachment', filename=att_basename)
            msg.attach(attpary)

    ##  下面开始真正的发送邮件了
    try:
        if transport == "TLS":
            s = smtplib.SMTP(smtp_server, smtp_port)
            #s.starttls()
        elif transport == "SSL":
            s = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            sys.exit(1)
        s.login(from_addr, password)
    except Exception, e:
        print e.message
    #下面两行放入try里面，vanke的邮箱就会报错，母鸡为什么呀。。。
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.quit()

def parseages():
    parser = optparse.OptionParser()
    parser.add_option("", "--subject", dest="subject", help="email subject",default=None)
    parser.add_option("", "--body", dest="body", help="email body",default=None)
    parser.add_option("", "--content", dest="content", help="email body content",default=None)
    parser.add_option("", "--to_addr", dest="to_addr", help="email to addr list,split with ;")
    parser.add_option("", "--attachment", dest="attachment", help="attachment file,default null",default=None)

    parser.add_option("", "--from", dest="from_addr", help="email sender",default=None)
    parser.add_option("", "--displayname", dest="displayname", help="sender displayname", default=None)
    parser.add_option("", "--passwd", dest="passwd", help="from passwd",default=None)
    parser.add_option("", "--smtp_server", dest="smtp_server", help="smtp_server",default=None)
    parser.add_option("", "--smtp_port", dest="smtp_port", help="smtp_port",default=None)
    parser.add_option("", "--transport", dest="transport", help="transport", default="SSL")

    parser.add_option("", "--default_vanke_email",action='store_true', dest="default_vanke_email", help="default_vanke_email",default=False)
    (option,args) = parser.parse_args()
    return (option,args)

def check_parser(subject, body, content, to_addr, attachment):
    _temp_list = [subject, body, content, to_addr, attachment]
    for i in range(len(_temp_list)):
        if _temp_list[i] is not None and type(_temp_list[i]) == type(""):
            _temp_list[i] = _temp_list[i].strip()
    if _temp_list[3] is not None and type(_temp_list[3]) != type([]):
        print "%s is not list" % _temp_list[3]
        sys.exit(1)
    if _temp_list[4] is not None and type(_temp_list[4]) != type([]):
        print "%s is not list" % _temp_list[4]
        sys.exit(1)
    return _temp_list[0],_temp_list[1],_temp_list[2],_temp_list[3],_temp_list[04],

def main():
    (options, args) = parseages()
    subject = options.subject
    body = options.body
    content = options.content
    to_addr = options.to_addr
    attachment = options.attachment
    in_from_addr = options.from_addr
    in_displayname = options.displayname
    in_password = options.passwd
    in_smtp_server = options.smtp_server
    in_smtp_port = options.smtp_port
    in_transport = options.transport
    default_vanke_email = options.default_vanke_email

    if attachment is not None:
        attachment = re.split(",|;", attachment)

    to_addr_list = re.split(",|;", to_addr)

    subject, body, content, to_addr, attachment = check_parser(subject, body, content, to_addr_list, attachment)

    if default_vanke_email:
        from_addr, displayname, password, smtp_server, smtp_port, transport = default_email_config_vanke()
    else:
        from_addr, displayname, password, smtp_server, smtp_port, transport = default_email_config_myqq()

    server_config_l = [ from_addr, displayname, password, smtp_server, smtp_port, transport ]
    in_server_config_l = [in_from_addr, in_displayname, in_password, in_smtp_server, in_smtp_port, in_transport]
    for i in range(len(in_server_config_l)):
        if in_server_config_l[i] is not None:
            server_config_l[i] = in_server_config_l[i]
    from_addr, displayname, password, smtp_server, smtp_port, transport = server_config_l[0], server_config_l[1], server_config_l[2], server_config_l[3], server_config_l[4], server_config_l[5]

    print "from_addr",from_addr
    #to_addr = ['yangy114@vanke.com','yangy114@vanke.com']
    #subject = "test"
    #body = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    #attachment = ["D:\\04.script\\temp\\1.json","D:\\04.script\\temp\\1.png"]
    send_email(from_addr, displayname, password, to_addr, smtp_server, smtp_port, transport, subject, body, attachment)

if __name__ == '__main__':
    main()