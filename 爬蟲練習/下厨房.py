# 步骤一：获取网页并打印响应状态码
import requests
import csv
from bs4 import BeautifulSoup

recipe_list = []

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
          }

index_url = 'https://www.xiachufang.com/explore/'
index = requests.get(index_url, headers = headers)

print(index.status_code)

# 步骤二：解析网页，解析请求到的网页数据并提取所有菜谱的标题、详情页链接和食材信息，最后打印所有菜谱信息

bs = BeautifulSoup(index.text, 'html.parser')
all_recipe = bs.find_all('div', class_='info pure-u')

for r in all_recipe:
    title = r.find('a').text.strip()
    link = 'http://www.xiachufang.com' + r.find('a')['href']
    material = r.find('p', class_='ing ellipsis').text.strip()
    
    recipe_dict = {
                    '標題': title,
                    '詳情頁': link,
                    '食材': material
                  }
    
    recipe_list.append(recipe_dict)
    
print(recipe_list)

# 步骤三：存储爬取的数据到 csv 文件

with open('recipe.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['標題','詳情頁','食材'])
    writer.writeheader()
    writer.writerows(recipe_list)