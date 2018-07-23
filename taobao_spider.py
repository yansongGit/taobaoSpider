#coding=utf-8
__author__ = 'yansong'
# 2018.07.12
# 抓取淘宝联盟 比率>10 ，描述、服务、物流3项参数高于或持平于同行业的商品图片。


import json
import demjson
import urllib2
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import sys
reload(sys)
sys.setdefaultencoding('utf8')

path_name = u'撞色拼接T恤'
Myname = u'T恤男'

# 创建文件夹
path = os.getcwd()   				     # 获取此脚本所在目录
new_path = os.path.join(path,path_name)
if not os.path.isdir(new_path):
	os.mkdir(new_path)


#url请求，获取响应的json数据，并将json数据转换成dict  采用selenium实现
def get_browser_text(url):
    #browser = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
    browser = webdriver.Firefox(executable_path="C:\\Program Files (x86)\\Mozilla Firefox\\geckodriver.exe")
    try:
        browser.get(url)
        print(browser.page_source)
        browserdata = browser.page_source
        browser.close()
        # res = r'<a .*?>(.*?)</a>'
        res = r'<pre .*?>(.*?)</pre>'
        json_data = re.findall(res, browserdata, re.S | re.M)
        print json_data
        for value in json_data:
            print value

        dict_data = demjson.decode(json_data)
        print 'dict_data:'
        print dict_data
        # print type(dict_data)
        return dict_data
    except:
        return ""


#url请求，获取响应的json数据，并将json数据转换成dict  采用 urllib2 实现
def getJSONText(url):
    try:
        page = urllib2.urlopen(url)
        data = page.read()
        #print (data)
        #print (type(data))
        #dict_data = json.loads(data)
        dict_data = demjson.decode(data)
        #print dict_data
        #print type(dict_data)
        return dict_data
    except:
        return ""


#url请求，获取响应的json数据，并将json数据转换成dict  采用 添加请求头、设置代理的方式 实现
def getJSONText2(url):
    try:
        proxies = {
            "http": "http://221.10.159.234:1337",
            "https": "https://60.255.186.169:8888",
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        data = requests.get(url, headers=headers,proxies=proxies).text
        print (data)
        print (type(data))
        # dict_data = json.loads(data)
        dict_data = demjson.decode(data)
        print dict_data
        print type(dict_data)
        return dict_data
    except:
        return ""


def getJSONText3(url):
    try:
        driver = webdriver.Chrome(executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        driver.get(url)  # 访问淘宝宝贝页面，获取cookie
        # driver.get(taobao_comment_url)  # 直接访问宝贝评论会被反爬虫检测到。上一步获得cookie后可得到评论数据
        print(driver.find_element_by_xpath('/html/body').text)
        data = driver.find_element_by_xpath('/html/body').text
        #data = requests.get(url, headers=headers,proxies=proxies).text
        print (data)
        print (type(data))
        # dict_data = json.loads(data)
        dict_data = demjson.decode(data)
        print dict_data
        print type(dict_data)
        return dict_data
    except:
        return ""


if __name__ == '__main__':

    #每一页的url 循环抓取60页
    for page in range(0, 60):
        url = ('http://pub.alimama.com/items/channel/qqhd.json?q=%s&channel=qqhd&_t=1531121449018&toPage=%d&perPageSize=50&shopTag=&t=1531125125414&_tb_token_=eeee6ee3be688&pvid=19_118.112.188.32_688_1531125125232'%(Myname,page))
        #url = ('http://pub.alimama.com/items/search.json?q=%E9%9E%8B%E5%AD%90&_t=1531368912715&auctionTag=&perPageSize=50&shopTag=yxjh&t=1531368913289&_tb_token_=e370663ebef17&pvid=10_118.112.188.32_9532_1531368912863')
        print url
        time.sleep(2)   #延时2秒，添加延时操作是因为淘宝有反爬虫机制，过于频繁的访问IP可能会被限制
        url_data=getJSONText(url)
        #一页中每件商品的标签信息
        for i in range(0, 50):
            time.sleep(1.1)
            try:
                #print type(url_data['data']['pageList'][i]['pictUrl'])
                pictUrl = url_data['data']['pageList'][i]['pictUrl']  #图片url
                sellerId = url_data['data']['pageList'][i]['sellerId']  # 商品id
                auctionUrl = url_data['data']['pageList'][i]['auctionUrl']  # 淘宝链接
                auctionId = url_data['data']['pageList'][i]['auctionId'] #   淘宝链接 =  'http://item.taobao.com/item.htm?id=%d'%(auctionId)
                tkRate = url_data['data']['pageList'][i]['tkRate']  # 比率
                zkPrice = url_data['data']['pageList'][i]['zkPrice']  # 价格

                # 需要抓取比率大于10.00的商品信息
                if tkRate > 10.00:
                    #time.sleep(1)
                    # print '详细信息:'
                    # print type(tkRate)
                    # print type(zkPrice)
                    # print '比率:%f' % (tkRate)
                    # print '价格:%f' % (zkPrice)
                    # print sellerId
                    # print auctionId
                    # print pictUrl
                    # print auctionUrl  # 淘宝链接
                    # print type(sellerId)

                    # 每件商品的子url (描述相符、发货速度、服务态度 等信息)
                    sub_url = ('http://pub.alimama.com/pubauc/searchPromotionInfo.json?oriMemberId=%d&blockId=&t=1531369204612&_tb_token_=e370663ebef17&pvid=10_118.112.188.32_760_1531368931581' % (sellerId))
                    sub_url_data = getJSONText(sub_url)  #获取店铺的 描述、服务、物流 信息

                    # print sub_url_data
                    # print (type(sub_url_data))
                    # print sub_url_data['invalidKey']
                    # print sub_url_data['data']
                    # print sub_url_data['data']['SellLevelPicture']
                    MerchandisGapBottom = sub_url_data['data']['MerchandisGapBottom']  # 描述相符   （true -- 与同行业相比低于    false -- 与同行业相比高于）
                    ConsignmentGapBottom = sub_url_data['data']['ConsignmentGapBottom']  # 发货速度
                    ServiceGapBottom = sub_url_data['data']['ServiceGapBottom']  # 服务态度
                    # print 'MerchandisGapBottom[0] 类型:'
                    # print type(MerchandisGapBottom[0])
                    # 如果3项评定参数都是 false 就将图片和相关信息抓取出来   任意一项参数为 true 都不符合要求
                    if ((not MerchandisGapBottom[0]) and (not ConsignmentGapBottom[0]) and (not ServiceGapBottom[0])):
                        time.sleep(1)

                        print MerchandisGapBottom
                        print ConsignmentGapBottom
                        print ServiceGapBottom
                        print type(MerchandisGapBottom)

                        MerchandisGap = sub_url_data['data']['MerchandisGap']  # 描述相符值
                        ConsignmentGap = sub_url_data['data']['ConsignmentGap']  # 发货速度值
                        ServiceGap = sub_url_data['data']['ServiceGap']  # 服务态度值

                        mypictUrl = 'http:' + pictUrl
                        picture_content = urllib2.urlopen(mypictUrl).read()
                        picture_name = auctionUrl + '.jpg'
                        print picture_name
                        time.sleep(1)


                        spider_info = 'url:' + url + '\n' + '  sub_url:' + sub_url + '\n' + '  淘宝链接:' + auctionUrl + '\n' + '  mypictUrl:' + mypictUrl + '\n\n'
                        try:
                            #写图片
                            index_num = picture_name.index('id=')
                            with open(path_name + '/' + picture_name[index_num:], 'wb') as code:
                                code.write(picture_content)
                            #写URL信息
                            with open(path_name + '/' + 'spider.txt', 'a') as spider_code:
                                spider_code.write(spider_info)
                        except (IOError, ZeroDivisionError), e:
                            print e
                            print "Error: 没有找到图片文件或读取文件失败"
                        else:
                            print "图片写入成功"

                        time.sleep(1)
            except (IndexError, KeyError, TypeError), e:
                print e
                print "每件商品信息读取失败"
            else:
                pass
                #print "每件商品的标签信息读取成功"


