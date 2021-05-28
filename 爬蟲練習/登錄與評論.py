# 步骤一：登录网站，获取登录后的 Cookies 信息
import csv
import requests
from bs4 import BeautifulSoup

data_list = []

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
          }

login_url = 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-login.php'

# username = input('用戶名：')
# password = input('密碼：')

# login_id = { 'log':username,
#             'pwd':password,
#             'wp-submit':'登录',
#             'redirect_to':'https://wordpress-edu-3autumn.localprod.oc.forchange.cn',
#             'testcookie':'1'
#            }

login_id = { 'log':'root',
            'pwd':'p%9*EIlVY2*7X%C&',
            'wp-submit':'登录',
            'redirect_to':'https://wordpress-edu-3autumn.localprod.oc.forchange.cn',
            'testcookie':'1'
           }

login = requests.post(login_url, headers=headers, data=login_id)
print(login.cookies)

# 步骤二：发送评论
comment_url = 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/all-about-the-future_01/'
comment_page = requests.get(comment_url, headers=headers, cookies = login.cookies)
comment = input('輸入評論：')

comment_req_url = 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-comments-post.php'
comment_data = {'comment': comment,
                'submit': '发表评论',
                'comment_post_ID': 13,
                'comment_parent': 0
               }

comment_post = requests.post(comment_req_url, headers=headers, data=comment_data, cookies = login.cookies)

# for verification
if comment_post.status_code == 200:
    print('發佈成功')
else:
    print('錯誤！請求狀態碼{}'.format(comment_post.status_code))
    
# 步骤三：爬取博客最新评论
n = 0

# 要多少爬多少
while n <= 99:
    url = comment_url + 'comment-page-{}/#comments'.format(9425-n)
    n += 1
    comment_page = requests.get(url, headers=headers, cookies = login.cookies)
    comment_page.encoding = 'utf-8'
    bs = BeautifulSoup(comment_page.text, 'html.parser')
    # all_comment = bs.find_all('div', class_='comment-content')
    
    # for c in all_comment:
    #     print(c.find('p').text)
    
    # 拓展：附上用戶名和評論時間，並生成表格
    all_comment = bs.find_all('article', class_='comment-body')
    for c in all_comment:
        commentor = c.find('footer').find('div', class_='comment-author vcard').find('b', class_='fn').text
        content = c.find('div', class_='comment-content').find('p').text
        comment_time = c.find('footer').find('div', class_='comment-metadata').find('a').find('time').text
        
        comment_dict = {'用戶名':commentor,
                        '評論':content,
                        '評論時間':comment_time
                        }
        
        data_list.append(comment_dict)
        
with open('renrenpinglun.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f,fieldnames=['用戶名','評論','評論時間'])
    writer.writeheader()
    writer.writerows(data_list)
