import requests
from lxml import etree
import csv
import time
from bs4 import BeautifulSoup
import os
import random
import get_headers


if os.path.exists("D://近五年全国地级市天气") == False:
    os.makedirs("D://近五年全国地级市天气")
os.chdir("D://近五年全国地级市天气")

city_name = []


def get_city_url():
    '''
        获取每个城市的url
    '''
    global city_name
    base_url = "http://www.tianqihoubao.com/lishi"
    response = requests.get(base_url, headers=get_headers.get_headers())
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    city_urls = html.xpath("//div[@class='citychk']//dd//a/@href")
    city_name = html.xpath("//div[@class='citychk']//dd//a/text()")
    city_urls = map(lambda url: "http://www.tianqihoubao.com"+url, city_urls)
    return city_urls


def get_page(url):
    """
        获取具体的天气信息
    """
    infos = []
    response = requests.get(url, headers=get_headers.get_headers())
    text = response.content.decode('gbk')
    soup = BeautifulSoup(text, 'lxml')
    trs = soup.find_all("tr")[1:]
    for tr in trs:
        tds = tr.find_all("td")
        data = ''.join(list(tds[0].stripped_strings)[0].split())
        state = ''.join(list(tds[1].stripped_strings)[0].split())
        temp = ''.join(list(tds[2].stripped_strings)[0].split())
        wind = ''.join(list(tds[3].stripped_strings)[0].split())
        info = {
            '日期': data,
            '天气状态': state,
            '气温': temp,
            '风力风向': wind
        }
        infos.append(info)
    return infos


def write_csv(path, infos):
    '''
        将数据写入csv文件
    '''
    titles = ['日期', '天气状态', '气温', '风力风向']
    with open(path, 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, titles)
        writer.writeheader()
        writer.writerows(infos)


def main():
    global city_name
    index = 0
    city_urls = list(get_city_url())
    for city_url in city_urls:
        print('正在爬取{}的历史天气'.format(city_name[index]))
        print("="*30)

        infos = []
        city_url = city_url.replace('.html', '/month/{}{:0>2d}.html')

        # 获取每个城市每年每月天气情况的url
        for year in range(2016, 2021):
            for month in range(1, 13):
                
                print(city_url.format(year, month))
                
                # 设置延时,防止造成服务器拒绝连接
                rand = random.randint(1, 3)
                time.sleep(rand)
                
                # 获取infos
                info = get_page(city_url.format(year, month))
                infos = infos+info

        # 写入数据
        path = city_name[index]+'.csv'
            
        write_csv(path, infos)
        rand = random.randint(60, 120)
        time.sleep(rand)
        index = index+1
        


if __name__ == '__main__':
    main()
