#coding=utf-8
import datetime
import os

import requests

import time
import sys
import codecs
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from dianping.Config import customInfo1, customInfo2
from utils.SMMailTool import sendSMMail


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

receivers = [ 'xxx@xx.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


historyCount = 0
successCount = 0
failCount=0
successTitle = ""
historyTitle = ""
failedTitle = ""


def doAction(name,productid,customInfo):
    Host = "m.dianping.com"
    actionURL = "https://m.dianping.com/beauty-salvia/try-center/tryresult.html?token=&longitude=*&lng=*&latitude=*&lat=*&dpid=*&channel=1&category=0&catid=50&utm_source=&cityid=1&ci=&mina_name=&productid="+str(productid)+"&source=&shopid=&mobile="+str(customInfo['mobile'])
    Origin = "https://m.dianping.com"

    Referer = "https://m.dianping.com/beauty-salvia/try-center/tryorder.html?token=&longitude=*&lng=*&latitude=*&lat=*&dpid=*&channel=1&category=0&catid=50&utm_source=&cityid=1&ci=&mina_name=&productid="+str(productid)
    header = {"Content-Type": "application/json;charset=UTF-8", "Origin": Origin, "Host": Host, "referer": Referer,
              "User-Agent": customInfo['useragent']}

    r1 = requests.get(actionURL, cookies=customInfo['cookies'], headers=header)
    # print(r1.text)
    global successCount
    successCount = successCount+1
    global successTitle
    successTitle = successTitle+name+"\n"




def requestList(customInfo):
    global historyCount
    global successCount
    global failCount
    global successTitle
    global historyTitle
    global failedTitle
    historyCount = 0
    successCount = 0
    failCount = 0
    successTitle = ""
    historyTitle = ""
    failedTitle = ""
    Host = "m.dianping.com"
    actionURL = "https://m.dianping.com/beautytry/productlist?channel=1&category=0&period=0&cityid=1&longitude=121.50572&latitude=31.31054&dpid=6139886069248743324&type=1"
    Origin = "https://m.dianping.com"

    Referer = "https://m.dianping.com/beauty-salvia/try-center/tryindex.html?channel=1&category=0&catid=50&cityid=1&longitude=121.50572&latitude=31.31054&dpid=6139886069248743324&utm_source=bwc&pushEnabled=1&type=1"
    header = {"Content-Type": "application/json;charset=UTF-8", "Origin": Origin, "Host": Host, "referer": Referer,
              "User-Agent": customInfo['useragent']}

    r1 = requests.get(actionURL, cookies=customInfo['cookies'], headers=header)
    print(r1.text)

    data = r1.json()

    goodProductList = data['data']['goodProductList']

    for item in goodProductList:
        hasRegister = item['hasRegister']
        name = item['name']
        productid = item['id']
        if hasRegister:

            historyCount=historyCount+1

            historyTitle = historyTitle + name+"\n"
            print(name+"已报名")
        else:
            doAction(name,productid, customInfo)

    hello = "尊敬的" + str(customInfo["username"]) + "用户您的当日霸王餐执行结果如下：\n"
    message1 = "********今日报名****************：" + str(successCount) + "条\n"
    message2 = "********历史成功报名************：" + str(historyCount) + "条\n"
    message3 = "********失败报名****************：" + str(failCount) + "条\n"
    message4 = "今日报名：\n" + successTitle
    message5 = "历史报名：\n" + historyTitle
    message6 = "报名失败：\n" + failedTitle
    message7 = "\n您的服务到期日为：" + customInfo['serviceendtime'] + "请及时联系管理员续费,过期后将无法收到霸王餐执行通知\n"
    message8 = "********请勿在浏览器中退出或者切换账户，否则会导致被系统登记的账户失效****************"

    mailContent = hello + message1 + message2 + message3 + message4 + message5 + message6 + message7 + message8

    titleMail = "免费变漂亮执行日报" + time.strftime("%Y%m%d")

    sendSMMail(titleMail, mailContent, customInfo['receivers'])



def startBeauty():
    
    requestList(customInfo1)


startBeauty()



