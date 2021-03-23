import os,re
from xpinyin import Pinyin

path = "D:\\2016-2020全国地级市天气"
os.chdir(path)

count={}
lack_data=[]

# 每个城市的csv表的数量
for filename in os.listdir(path):
    filename=''.join(re.findall(r'[^0-9]',filename))[:-9]
    count.setdefault(filename,0)
    count[filename]+=1
    
# 查找有缺失数据的城市
for k, v in count.items():
    if v != 60:
        lack_data.append(k)

lack_data_url=[]  

# 重构url
p=Pinyin()     
for data in lack_data:
    lack_data_url.append(''.join(['http://www.tianqihoubao.com/lishi/',p.get_pinyin(data,''),'.html']))

# 剩余缺失数据的城市的数量
print(lack_data_url)
print(len(lack_data_url))
print(len(lack_data))
    


