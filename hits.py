from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from pymongo import MongoClient

# с этими модулями пока не подружился :))
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument('--headless')
import time

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

assert 'М.Видео' in driver.title
time.sleep(5)

# победить кнопку c предложением включить рассылку не удалось...
# Данные кода различаются между обычным браузером и chromedriver
# версия браузера 88. хромдайвер 88...
try:
    button = driver.find_element_by_class_name('PushTip-close')
    button.click()
except:
    print('нет кнопки рассылки')

# С окном - предложением подписки та же история. Не срабатывает
try:
    button = driver.find_element_by_id('Cross')
    button.click()
except:
    print('нет кнопки подписки')

data = driver.find_element_by_xpath("//div[@class='accessories-carousel-holder carousel tabletSwipe']")
i = 1
while True:
    try:
        button = data.find_element_by_class_name('sel-hits-button-next')
        button.click()
        time.sleep(2)
        print(f'Нажали {i} раз')
        i += 1
        try: # "Костыль" для остановки нажатия кнопки. День убил, но ни чего другого сделать не смог...
            stops = data.find_element_by_class_name('disabled')
            stops.click()
            break
        except:
            pass
    except:
        break

hits = data.find_elements_by_class_name('gallery-list-item')

client = MongoClient('localhost', 27017) # подключаем базу
db = client['shop']
shop_hits = db.shop_hits
for hit in hits:
    a = len(hits)
    sale_hits = {}
    link = hit.find_element_by_class_name('sel-product-tile-title').get_attribute('href')
    value = hit.find_element_by_class_name('sel-product-tile-title').get_attribute('data-product-info')

    param = json.loads(value)


    sale = float(param['productPriceLocal'])
    name = hit.find_element_by_tag_name('h4').get_attribute('title')
    sale_hits['name'] = name
    sale_hits['sale'] = sale
    sale_hits['link'] = link
    print(sale_hits) # смотрим, что мы записываем в базу
    shop_hits.insert_one(sale_hits)
driver.quit()