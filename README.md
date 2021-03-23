# 2016-2020Chinese-Weather-Analysis

一、爬取数据
1.确定爬虫要获取的数据：2016-2020年全国363个城市每天的天气情况(城市名、日期、天气状况、气温、风力风向)
2.爬取的网站：天气后报网(http://www.tianqihoubao.com/lishi)
3.要使用的技术：lxml、BeautifulSoup、requests、(多线程queue)
4.分析待抓取数据的网站：
  1)打开天气后报网(http://www.tianqihoubao.com/lishi)，
