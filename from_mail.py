from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from pymongo import MongoClient


from time import sleep

chrome_options = Options()
#chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.yandex.ru/')
assert 'Яндекс.Почта' in driver.title
button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'HeadBanner-Button-Enter'))
)
button.click()
assert 'Авторизация' in driver.title
sleep(1)
user = input('Введите ваш логин от mail.yandex.ru: ')
elem = driver.find_element_by_id('passp-field-login')
elem.send_keys(user)
elem.send_keys(Keys.RETURN)
sleep(1)
passwd = input('Введите ваш пароль от mail.yandex.ru: ')
elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys(passwd)
elem.send_keys(Keys.RETURN)

while True:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'js-message-load-more'))
        )
        button.click()
    except Exception as e:
        print('Все письма зашружены\n')
        break
messages_links = driver.find_elements_by_class_name('mail-MessageSnippet')

# Собираем все ссылки на письма в отдельный список,
# т.к. напрямую получать их в цикле с обработкой не вышходит. Выдает только первую ссылку в цикле.
links = []
for message_link in messages_links:
    links.append(message_link.get_attribute('href'))

i = 1
client = MongoClient('localhost', 27017)
db = client['emails']
mails = db.mails

for link in links:
    message = {}
    driver.get(link)
    sleep(1)
    subj = driver.find_element_by_class_name('mail-Message-Toolbar-Subject_message').text
    sender = driver.find_element_by_class_name('mail-Message-Sender-Email').text
    data = driver.find_element_by_class_name('ns-view-message-head-date').text
    text = driver.find_element_by_class_name('mail-Message-Body-Content').text
    message['subj'] = subj
    message['sender'] = sender
    message['data'] = data
    message['text'] = text
    mails.insert_one(message)
    print(f'Сохранено письмо №{i}')
    i += 1
    sleep(1)

driver.quit()
