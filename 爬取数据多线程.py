import requests
from lxml import etree
import csv
import time
from bs4 import BeautifulSoup
import os
import random
import get_headers # 放置数个headers信息,设置反反爬虫,随机返回一个headers信息
from queue import Queue
import threading


# 如果该文件夹不存在则创建，存在则什么都不做
os.makedirs("D:\\2016-2020全国地级市天气(月)",exist_ok=True)

os.chdir("D:\\2016-2020全国地级市天气(月)")

# 获取所需的详情页面的url
class Producer(threading.Thread):
    def __init__(self,details_url_queue,city_url_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.details_url_queue=details_url_queue
        self.city_url_queue=city_url_queue
        
        
    # threading.thread 有 run 方法，会从run()方法开始执行函数    
    def run(self):
        while True:
            if self.city_url_queue.empty():
                break
            url = self.city_url_queue.get()
            self.get_details_url(url)
        
    def get_details_url(self,url):
        # 获取每个城市每年每月天气情况的url    
        url = url.replace('.html', '/month/{}{:0>2d}.html')
        for year in range(2016,2021):
            for month in range(1, 13):
                self.details_url_queue.put(url.format(year,month))
            
# 获取所需的数据   
class Consumer(threading.Thread):
    def __init__(self,details_url_queue,city_url_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.details_url_queue=details_url_queue
        self.city_url_queue=city_url_queue
    
    def run(self):
        while True:
            if self.city_url_queue.empty() and self.details_url_queue.empty():
                break
            url = self.details_url_queue.get()
            self.get_page(url)
            
    def get_page(self,url):
        """
            获取具体的天气信息
        """
        print(url)
        infos = []
        response = requests.get(url, headers=get_headers.get_headers())
        text = response.content.decode('gbk')
        soup = BeautifulSoup(text, 'lxml')
        # 获取 城市 日期 天气状态 气温 风力风向信息
        city = list(soup.find('div',attrs={"id":"s-calder","class":"box"}).stripped_strings)[0]
        city = ''.join(re.findall(r'[^0-9]',city))[:-9]
        trs = soup.find_all("tr")[1:]
        for tr in trs:
            tds = tr.find_all("td")
            date = ''.join(list(tds[0].stripped_strings)[0].split())
            state = ''.join(list(tds[1].stripped_strings)[0].split())
            temp = ''.join(list(tds[2].stripped_strings)[0].split())
            wind = ''.join(list(tds[3].stripped_strings)[0].split())
            info = {
                '城市': city,
                '日期': date,
                '天气状态': state,
                '气温': temp,
                '风力风向': wind
            }
            infos.append(info)
        rand = random.randint(1, 3)
        time.sleep(rand)
        # 将数据写入csv
        path = "D:\\2016-2020全国地级市天气(月)\\"+city[:-4]+'.csv'
        titles = ['城市','日期', '天气状态', '气温', '风力风向']
        with open(path, 'w', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, titles)
            writer.writeheader()
            writer.writerows(infos)
        
def main():
    # 创建两个队列，放置线程
    details_url_queue = Queue(1000)
    city_url_queue = Queue(363)
    
    获取每个城市的url
    base_url = "http://www.tianqihoubao.com/lishi"
    response = requests.get(base_url, headers=get_headers.get_headers())
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    city_urls = html.xpath("//div[@class='citychk']//dd//a/@href")
    city_urls = list(map(lambda url: "http://www.tianqihoubao.com"+url, city_urls))
    for city_url in city_urls:
        city_url_queue.put(city_url)

    
    # 多线程启动
    t1=Producer(details_url_queue,city_url_queue)
    t1.start()
    
    for i in range(7):
        t=Consumer(details_url_queue,city_url_queue)
        t.start()

    



if __name__ == '__main__':
    main()
