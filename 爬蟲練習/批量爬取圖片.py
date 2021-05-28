# 步骤一：获取网页：获取书籍列表页前 3 页的链接
import requests
from bs4 import BeautifulSoup
import csv

book_list = []

target = 'https://wp.forchange.cn/resources/page/'
n = 1

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
          }

# 要幾頁爬幾頁
while n <= 3:
    webpage = target + str(n)
    n += 1
    res = requests.get(webpage, headers = headers)
    
    # print(webpage)
    print(res.status_code)

    # 步骤二：解析网页，提取书籍名称和书籍封面链接
    bs = BeautifulSoup(res.text, 'html.parser')
    book_image = bs.find_all('div', class_='media-pic')
    
    for i in book_image:
        book_title = i.find('img')['alt']
        image_link = i.find('img')['data-src']
        
        book_dict = {
                    '書名':book_title,
                    '封面鏈接':image_link
                    }
        book_list.append(book_dict)
        
        # 步骤三：存储数据，存储书籍封面，写入图片文件
        
        # 通过书籍封面链接请求书籍封面，并将结果赋值给变量 image_res
        image_res = requests.get(image_link)
        # 把书籍封面的响应内容以二进制数据的形式返回
        image = image_res.content
        
        # 以无需关闭文件的形式打开图片，图片内容以二进制格式只写
        with open('./批量獲取圖片/{}.png'.format(book_title), 'wb') as f:
            # 将二进制数据写入文件
            f.write(image)

        # 打印封面保存信息
        print('{}封面已保存'.format(book_title))

        
print(book_list)

with open('封面圖鏈接表.csv','w',encoding='utf-8') as d:
    writer = csv.DictWriter(d, fieldnames=['書名','封面鏈接'])
    writer.writerows(book_list)