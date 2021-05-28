import requests

res = requests.get('https://www.uni-bonn.de/de')
code = res.status_code
print(code)

res.encoding = 'utf-8'

text = res.text
print(text)