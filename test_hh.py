from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests

superjob = []  # Заявляем словарь для данных с сайта https://www.superjob.ru
hh = []  # Заявляем словарь для данных с сайта https://hh.ru

#заголовок взят из моего гугл хрома. Но пробовал и без него
headers = {
    'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

print('\nваша ссылка\n')
html = requests.get('https://hh.ru/search/vacancy?st=searchVacancy&text=python',headers=headers)
pprint(html.text)

print('\nссылка из браузера\n')
html1 = requests.get('https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&area=113&from=cluster_area&showClusters=true')
pprint(html1.text)

# --------------------    результат вывода у меня   -----------------------

# ваша ссылка

# ('<html>\r\n'
# '<head><title>404 Not Found</title></head>\r\n'
# '<body>\r\n'
# '<center><h1>404 Not Found</h1></center>\r\n'
# '<hr><center>nginx</center>\r\n'
# '</body>\r\n'
# '</html>\r\n')

# ссылка из браузера

#('<html>\r\n'
# '<head><title>404 Not Found</title></head>\r\n'
# '<body>\r\n'
# '<center><h1>404 Not Found</h1></center>\r\n'
# '<hr><center>nginx</center>\r\n'
# '</body>\r\n'
# '</html>\r\n')
