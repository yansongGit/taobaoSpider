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
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import sys
reload(sys)
sys.setdefaultencoding('utf8')

path_name = u'束脚牛仔裤男'
Myname = u'小脚牛仔裤男'

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


# 获取单个商品的HTML代码并用正则匹配出描述、服务、物流3项参数  采用urllib2
def getHTMLText(url):
    try:
        data = urllib2.urlopen(url).read()
        res = r'<dd class="tb-rate-(.*?)"'
        data_list = re.findall(res, data, re.S | re.M)
        print type(data_list)
        print data_list[0]
        #for value in mm:
        #   print value
        return data_list
    except:
        return  ""


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

def mytaobao_spider():
    #每一页的url  循环抓取50页
    for page in range(0, 60):
        url = ('http://pub.alimama.com/items/channel/qqhd.json?q=%s&channel=qqhd&_t=1531121449018&toPage=%d&perPageSize=50&shopTag=&t=1531125125414&_tb_token_=eeee6ee3be688&pvid=19_118.112.188.32_688_1531125125232'%(Myname,page))
        #url = ('http://pub.alimama.com/items/search.json?q=%E9%9E%8B%E5%AD%90&_t=1531368912715&auctionTag=&perPageSize=50&shopTag=yxjh&t=1531368913289&_tb_token_=e370663ebef17&pvid=10_118.112.188.32_9532_1531368912863')
        print url
        time.sleep(2)  #延时2秒，添加延时操作是因为淘宝有反爬虫机制，过于频繁的访问IP可能会被限制
        url_data=getJSONText(url)
        #一页中每件商品的标签信息
        for i in range(0, 50):
            time.sleep(1)
            try:
                #print type(url_data['data']['pageList'][i]['pictUrl'])
                pictUrl = url_data['data']['pageList'][i]['pictUrl']  #图片url
                sellerId = url_data['data']['pageList'][i]['sellerId']  # 商品id
                auctionUrl = url_data['data']['pageList'][i]['auctionUrl']  # 淘宝链接
                auctionId = url_data['data']['pageList'][i]['auctionId'] #   淘宝链接 =  'http://item.taobao.com/item.htm?id=%d'%(auctionId)
                tkRate = url_data['data']['pageList'][i]['tkRate']  # 比率
                zkPrice = url_data['data']['pageList'][i]['zkPrice']  # 价格

                #需要抓取比率大于10.00的商品信息
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
                    print auctionUrl

                    # 每件商品的子url (描述相符、发货速度、服务态度 等信息)
                    #sub_url = ('http://pub.alimama.com/pubauc/searchPromotionInfo.json?oriMemberId=%d&blockId=&t=1531369204612&_tb_token_=e370663ebef17&pvid=10_118.112.188.32_760_1531368931581' % (sellerId))
                    sub_url = auctionUrl #每件商品的淘宝url
                    sub_url_data = getHTMLText(sub_url)  #获取店铺的 描述、服务、物流 信息
                    print type(sub_url_data)
                    print len(sub_url_data)

                    #如果返回的是空字符串, 则说明没有取到我们想要的字段，是因为淘宝有不同的页面，对于这种页面我们需要进一步分析下面的url
                    if (len(sub_url_data) == 0):
                        info_url = ('https://world.taobao.com/item/%d.htm' % (auctionId))
                        info_data = urllib2.urlopen(info_url).read()
                        res_info = r'<li class="([^s].*?)<img'
                        tmp_url_data = re.findall(res_info, info_data, re.S | re.M)
                        print "tmp_url_data:"
                        for value1 in tmp_url_data:
                            print value1

                        sub_url_data=[]
                        score_list = [x[0:4] for x in tmp_url_data]  #截取前面5位
                        print 'new_list:'
                        for score in score_list:
                            print score
                            if score == 'down':
                                score = 'lower'    #d第一种页面与第二种页面返回的店铺评定信息不同，需转换成统一的方便后面处理，将 down 转换为 lower
                            sub_url_data.append(score)

                        print '替换后的list元素:'
                        for level_data in sub_url_data:
                            print level_data
                    #如果3项评定参数都不是‘lower’ 就将图片和相关信息抓取出来   任意一项参数为‘lower’都不符合要求
                    if((not(sub_url_data[0] == 'lower' ) ) and (not(sub_url_data[1] == 'lower' ) ) and (not(sub_url_data[2] == 'lower' ) ) ):
                        #for value in sub_url_data:
                         #   print value

                        mypictUrl = 'http:' + pictUrl  #图片url
                        picture_content = urllib2.urlopen(mypictUrl).read()
                        picture_name = auctionUrl + '.jpg' #拼接图片名称
                        print picture_name
                        time.sleep(1)

                        #需要写入文件的信息
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




if __name__ == '__main__':
    mytaobao_spider()





