#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
from time import sleep

mail_host="smtp.xxx.com"  #设置服务器
mail_user="xxx"    #用户名
mail_pass="xxxx"   #口令
sender = 'xxx@xxx.com'
mail_port = 994



def sendSMMail(title, content, receivers):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = ";".join(receivers)

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    # smtpObj = smtplib.SMTP()
    smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)

    # smtpObj.connect(mail_host, mail_port)

    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

    print("邮件发送成功")

    smtpObj.quit()



