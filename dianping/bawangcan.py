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



def PreApply(activityId,customInfo, proxy):
    Host = "m.dianping.com"
    Origin = "https://m.dianping.com"

    Referer = "https://m.dianping.com/mobile/dinendish/success/"+str(activityId)+"?desc=%E6%88%90%E5%8A%9F&prized="

    data1 = {"activityId": activityId, "env": 1}
    PreApplyURL = "https://m.dianping.com/mobile/dinendish/apply/getPreApply"
    header = {"Content-Type": "application/json;charset=UTF-8", "Origin": Origin, "Host": Host, "referer": Referer,
              "User-Agent": customInfo['useragent']}

    r1 = requests.post(PreApplyURL, cookies=customInfo['cookies'], params=data1, headers=header, proxies=proxy)

    result = r1.json()

    data = result['data']
    try:
        activityStatus = data['activityStatus']
        title = data['title']
        if activityStatus != 1:
            print(title + " 已报名")
            return
        else:

            time.sleep(2)
            doAction(title, activityId, customInfo, proxy)
    except Exception as e:
        print(e)

    time.sleep(2)







def doAction(title,activityId,customInfo, proxy):
    Host = "m.dianping.com"
    Origin = "https://m.dianping.com"

    Referer = "https://m.dianping.com/mobile/dinendish/apply/"+str(activityId)+"?a=1&source=null&utm_source=null&showShopId=0&token=%2a&uiwebview=1"

    data1 = {"offlineActivityId": activityId, "env": 1,"marryDayStr":"2022/10/05","marryStatus":"0",'extraCount':'0','isShareSina':'True','isShareQQ':'True'}
    actionURL = "https://m.dianping.com/mobile/dinendish/apply/doApplyActivity"
    header = {"Content-Type": "application/json;charset=UTF-8", "Origin": Origin, "Host": Host, "referer": Referer,
              "User-Agent": customInfo['useragent']}

    r1 = requests.get(actionURL, cookies=customInfo['cookies'], params=data1, headers=header,proxies=proxy)
    print(r1.text)

    try:
        result = r1.json()
        code = result['data']['code']
        desc = result['data']['desc']

        if code == 402:
            print("报名失败:" + desc)
            global failCount
            failCount = failCount + 1
            global failedTitle
            failedTitle = failedTitle + title + "\n"
            failedTitle = failedTitle + desc + "\n"
        else:
            global successCount
            successCount = successCount + 1
            global successTitle
            successTitle = successTitle + title + "\n"
    except Exception as e:
        print(e)
    time.sleep(2)



def starChoujiang(page,proxy, customInfo):

    Host = "m.dianping.com"
    Origin = "https://m.dianping.com"

    Referer = "https://m.dianping.com/app/app-community-free-meal/index.html?utm_source=qgzq&from=m_richbutton_1"



    url_list = "https://m.dianping.com/activity/static/list"
    header = {"Content-Type": "application/json;charset=UTF-8", "Origin": Origin, "Host": Host, "referer": Referer,
              "User-Agent": customInfo['useragent']}


    data = {'page':page,"cityid":"1","latitude":"","regionParentId":"0","regionId":"0","type":"1","sort":"0","filter":"0"}

    r1 = requests.get(url_list, cookies=customInfo['cookies'], params=data, headers=header, proxies=proxy)
    # print(r1.text)

    result = r1.json()

    try:
        mobileActivitys = result['data']['mobileActivitys']
    except Exception as e:
        print(e)
        return

    print("第" + str(page) + "页一共" + str(len(mobileActivitys)) + "个餐厅")
    i=0


    for item in mobileActivitys:
        offlineActivityTagDTOList= item['offlineActivityTagDTOList']

        applyed=item['applyed']
        offlineActivityId = item['offlineActivityId']

        title = item['title']

        if applyed:
            print(title+" 已报名")
            global historyTitle
            historyTitle=historyTitle+title+"\n"
            global historyCount
            historyCount=historyCount+1

            continue


        hasvip = customInfo["hasvip"]
        if hasvip:
            print("第" + str(page) + "页 第 " + str(i) + "个 开始抽奖：" + title)
            PreApply(offlineActivityId, customInfo, proxy)
        else:
            if len(offlineActivityTagDTOList)<=0:

                print("第"+str(page)+"页 第 "+str(i)+"个 开始抽奖："+title)
                PreApply(offlineActivityId, customInfo, proxy)
        i=i+1


def checkin(customInfo):
    url = "https://m.dianping.com/mobile/event/arro/checkin"

    Host = "m.dianping.com"
    Origin = "https://m.dianping.com"

    Referer = "https://m.dianping.com/app/app-community-free-meal/index.html?utm_source=qgzq&from=m_richbutton_1"


    header = {"Content-Type": "application/json;charset=UTF-8", "Origin": Origin, "Host": Host, "referer": Referer,
              "User-Agent": customInfo['useragent']}

    data = {}

    r1 = requests.get(url, cookies=customInfo['cookies'], params=data, headers=header)

    data = r1.json()
    msg = data['msg']
    print(msg)
    availableIntegral = msg['availableIntegral']
    dayNum = msg['dayNum']

    result = "当前可用霸气值：%d  连续签到 %d天  \n"%(availableIntegral,dayNum )
    print(result)


    return result


def startbawangcanOnePerson(proxy,customInfo):

    try:

        print("*******开启霸王餐*******")

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
        failedTitle=""
        message0 = ""

        try:
            message0 = checkin(customInfo)
            time.sleep(5)
        except Exception as e:
            print(e)


        serviceendtime = customInfo['serviceendtime']

        n_time = datetime.datetime.now()

        end_time = datetime.datetime.strptime(serviceendtime,'%Y-%m-%d')

        if n_time <= end_time:
            for i in range(1, 9):
                starChoujiang(i, proxy,customInfo)

            hello = "尊敬的" + str(customInfo["username"]) + "用户您的当日霸王餐执行结果如下：\n"
            message1 = "********今日报名****************：" + str(successCount) + "条\n"
            message2 = "********历史成功报名************：" + str(historyCount) + "条\n"
            message3 = "********失败报名****************：" + str(failCount) + "条\n"
            message4 = "今日报名：\n" + successTitle
            message5 = "历史报名：\n" + historyTitle
            message6 = "报名失败：\n" + failedTitle
            message7 = "\n您的服务到期日为：" + customInfo['serviceendtime'] + "请及时联系管理员续费,过期后将无法收到霸王餐执行通知\n"
            message8 = "********请勿在浏览器中退出或者切换账户，否则会导致被系统登记的账户失效****************"

            mailContent = hello +message0+ message1 + message2 + message3 + message4 + message5 + message6 + message7+message8
        else:

            mailContent = "您的霸王餐服务已于" + customInfo['serviceendtime'] + "到期，请及时联系管理员续费。"




        print(mailContent)



        titleMail = "霸王餐执行日报" + time.strftime("%Y%m%d")

        sendSMMail(titleMail,mailContent,customInfo['receivers'])

    except Exception as e:
        print(e)





def startbawangcan():
    
   
    proxy1 = getProxy()
    startbawangcanOnePerson(proxy1,customInfo1)







def getProxy():

    r = requests.get("http://xxx.com:8090/get/")
    data = r.json()
    proxy = data['proxy']
    proxies = {


    }

    return proxies

def getUsefulProxy():
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    proxy = getProxy()
    html = requests.head('http://segmentfault.com')  # 用head方法去请求资源头部
    if html.status_code == 200:  # 状态码
        return proxy

    proxy = getProxy()
    html = requests.head('http://segmentfault.com')  # 用head方法去请求资源头部
    if html.status_code == 200:  # 状态码
        return proxy

    proxy = getProxy()
    html = requests.head('http://segmentfault.com')  # 用head方法去请求资源头部
    if html.status_code == 200:  # 状态码
        return proxy

    return proxy




startbawangcan()


