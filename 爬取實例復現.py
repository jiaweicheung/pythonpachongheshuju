import csv
import requests
from bs4 import BeautifulSoup

# 设置列表，用以存储每种食物的信息
foodlist = []

# 使用 for 循环遍历取值范围为 1~3 的数据
for t in range(1,4):
    # 使用 for 循环遍历取值范围为 1~3 的数据
    for p in range(1,4):
        # 设置要请求的网页链接
        url = 'http://www.boohee.com/food/group/{}?page={}'.format(t, p)
        # 请求网页
        webpage = requests.get(url)
        # 解析请求到的网页内容
        bs = BeautifulSoup(webpage.text, 'html.parser')
        # 提取食物类别
        foodtype = bs.find('div', class_='widget-food-list pull-right').find('h3').text.strip()
        # 搜索网页中所有包含食物信息的 Tag
        foodinfo = bs.find_all('div', class_='text-box pull-left')

        # 使用 for 循环遍历搜索结果
        for f in foodinfo:
            # 提取食物名
            foodname = f.find('a')['title']
            # 提取食物热量
            foodcal = f.find('p').text[3:]
            # 提取食物链接
            foodlink = 'http://www.boohee.com/{}'.format(f.find('a')['href'])

            # 将信息添加到字典中
            fooddict = {'食物类别': foodtype,'食物名': foodname,'食物热量': foodcal,
                        '食物链接': foodlink}
            # 将每种食物的信息添加至列表中
            foodlist.append(fooddict)
            # 打印食物的信息
            print(fooddict)

# 新建 csv 文件，用以存储食物信息
with open('food.csv', 'w', encoding='utf-8') as c:
    # 将文件对象转换成 DictWriter 对象
    writer = csv.DictWriter(c, fieldnames = ['食物类别', '食物名', '食物热量', '食物链接'])
    # 写入表头与数据
    writer.writeheader()
    writer.writerows(foodlist)