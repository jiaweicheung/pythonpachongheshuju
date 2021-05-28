import csv
import requests
from bs4 import BeautifulSoup

# 设置列表，用以存储每条评论的信息
datalist = []

# 设置登录网站的请求网址
loginurl = 'https://wp.forchange.cn/wp-admin/admin-ajax.php'
# 输入用户的账号密码
# username = input('输入用户的账号:')
# password = input('输入用户的密码:')
# 设置登录请求的请求体数据
loginid = {'action': 'ajaxlogin',
    'username': 'bbking',
    'password': '896VEkHc7rmCtmX',
    'remember': 'true'}

# 请求登录网站
req = requests.post(loginurl, data=loginid)

# 设置要请求的书籍网页链接
url = 'https://wp.forchange.cn/psychology/11069/comment-page-1/'
# 携带获取到的 Cookies 信息请求书籍网页
res = requests.get(url, cookies=req.cookies)
# 解析请求到的书籍网页内容
bs = BeautifulSoup(res.text, 'html.parser')
# 搜索网页中所有包含评论的 Tag
comment = bs.find_all('div', class_='comment-txt')

# 使用 for 循环遍历搜索结果
for c in comment:
    # 提取用户名
    name = c.find('cite', class_='fn').text[:-2]
    # 提取评论时间
    time = c.find('p', class_='date').text
    # 提取评论内容
    co = c.find('div', class_='bd').find('p').text

    # 将评论的信息添加到字典中
    codict = {'用户名': name,
             '评论时间': time,
             '评论内容': co
             }
    # 打印评论的信息
    print(codict)
    # 存储每条评论的信息
    datalist.append(codict)

# 新建 csv 文件，用以存储评论的信息
with open('comment.csv','w',encoding='utf-8') as d:
    # 将文件对象转换成 DictWriter 对象
    writer = csv.DictWriter(d, fieldnames=['用户名', '评论时间', '评论内容'])
    # 写入表头与数据
    writer.writeheader()
    writer.writerows(datalist)