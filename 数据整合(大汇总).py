import os,csv

path = "D:\\2016-2020全国地级市天气(城市)"
os.chdir(path)

infos=[]
for filename in os.listdir(path):
    print("正在整合:", filename)
    with open(filename,'r',encoding='utf-8') as fp:
        csv_read = csv.reader(fp)
        title = next(csv_read)
        for info in csv_read:
            infos.append(info)
            
os.makedirs("D:\\2016-2020全国地级市天气(大汇总)", exist_ok=True)
new_path = ''.join(["D:\\2016-2020全国地级市天气(大汇总)\\2016-2020全国地级市天气大汇总.csv"])
with open(new_path,'w',encoding='utf-8',newline='') as fp:
    writer = csv.writer(fp, title)
    writer.writerow(title)
    for info in infos:
        writer.writerow(info)

                    