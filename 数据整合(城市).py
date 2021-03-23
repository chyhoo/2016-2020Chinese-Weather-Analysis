# 生成363张以城市为名的csv表

import os
import re
import csv

path = "D:\\2016-2020全国地级市天气(月)"
os.chdir(path)

# csv表头信息
titles = ['城市', '日期', '天气状态', '气温', '风力风向']

# 获取城市名
cities = []
for filename in os.listdir(path):
    filename = ''.join(re.findall(r'[^0-9]', filename))[:-9]
    if filename not in cities:
        cities.append(filename)

# 创建每个城市天气信息带表头的空csv文件
os.makedirs("D:\\2016-2020全国地级市天气(城市)", exist_ok=True)
for city in cities:
    new_path = ''.join(["D:\\2016-2020全国地级市天气(城市)\\", city, '.csv'])
    with open(new_path, 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, titles)
        writer.writeheader()

# 将数据追加进csv表中
# 按城市整合 一个城市一张csv表
for filename in os.listdir(path):
    print("正在整合:", filename)
    infos = []
    read_path = ''.join(["D:\\2016-2020全国地级市天气(月)\\", filename])
    
    # 获取每张csv表的数据
    with open(read_path, 'r', encoding='utf-8') as fp:
        csv_read = csv.reader(fp)
        title = next(csv_read)
        for info in csv_read:
            infos.append(info)
    # 将数据追加进相应的csv表中
    city_name = ''.join(re.findall(r'[^0-9]', filename))[:-9]
    csv_path = ''.join(["D:\\2016-2020全国地级市天气(城市)\\", city_name, '.csv'])
    with open(csv_path, 'a+', encoding='utf-8', newline='') as fp:
        csv_write = csv.writer(fp, titles)
        for info in infos:
            csv_write.writerow(info)
