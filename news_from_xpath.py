from lxml import html
import requests
from datetime import datetime
import re

header = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
main_link1 = 'https://lenta.ru'
main_link2 = 'https://mail.ru/'

months = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December'
}


def news_from_lenta():
    news_lenta = "Что-то пошло не так. Sorry..."
    try:
        request = requests.get(main_link1, headers=header)
        get_html = html.fromstring(request.text)

        # Список ссылок
        link_list = get_html.xpath(
            "//div[@class='first-item']/a/@href | //div[contains(@class, 'span8')]//div[@class='item']/a/@href"
        )

        # Заголовки
        name_list = get_html.xpath(
            "//div[@class='first-item']//h2/a/text() | //div[contains(@class, 'span8')]//div[@class='item']/a/text()"
        )

        # Время публикации
        time_list = get_html.xpath(
            "//div[@class='first-item']//time/@datetime | //div[contains(@class, 'span8')]//div[@class='item']//time/@datetime"
        )
        # Приводим время публикации в нужный формат
        time_prep = []
        for get_time in time_list:
            t_pat = re.compile('\s*(\d{1,2}:\d{1,2})')
            d_pat = re.compile(',\s(\d+)\s')
            m_pat = re.compile('\d+\s(\w+)\s\d+')
            y_pat = re.compile('\s\w+\s(\d+)')

            ti = re.findall(t_pat, get_time)[0]
            d = re.findall(d_pat, get_time)[0]
            m = re.findall(m_pat, get_time)[0]
            if m in months:
                m = months[m]
            y = re.findall(y_pat, get_time)[0]
            time = datetime.strptime(ti + ' ' + d + ' ' + m + ' ' + y, '%H:%M %d %B %Y')
            time_format = "%Y-%m-%d %H:%M:%S"
            time_f = f"{time:{time_format}}"

            time_prep.append(time_f)
        # Складываем новости
        news_lenta = []
        for i in range(len(name_list)):
            news_data = {}
            news_data['news_from'] = main_link1
            news_data['news_name'] = name_list[i].replace('\xa0', ' ')
            news_data['news_link'] = main_link1 + link_list[i]
            news_data['publish_at'] = time_prep[i]
            news_lenta.append(news_data)


    except requests.exceptions.ConnectionError:
        news_lenta = "No connection to site"

    finally:
        return news_lenta

def news_from_mail():
    news_mail = "Что-то пошло не так. Sorry..."
    try:
        request = requests.get(main_link2, headers=header)
        get_html = html.fromstring(request.text)

        # Заголовки
        name_list = get_html.xpath(
            "//div[contains(@class, 'news-item_main')]//h3/text() | //div[contains(@class, 'news-item_inline')]//a/text()"
        )
        # Список ссылок
        link_list = get_html.xpath(
            "//div[contains(@class, 'news-item_main')]//a/@href | //div[contains(@class, 'news-item_inline')]//a/@href"
        )

        # Складываем новости
        news_mail = []
        for i in range(len(name_list)):
            news_data = {}
            news_data['news_from'] = main_link2
            news_data['news_name'] = name_list[i].replace('\xa0', ' ')
            news_data['news_link'] = link_list[i]
            if 'https:' in link_list[i]:
                news_data['publish_at'] = get_time_mail(link_list[i])
                news_mail.append(news_data)

    except requests.exceptions.ConnectionError:
        news_mail = "No connection to site"

    finally:
        return news_mail


# функция получения даты публикации новости с mail.ru
def get_time_mail(link):
    time_format = "%Y-%m-%d %H:%M:%S"
    time_f = f"{datetime.now():{time_format}}"
    try:
        request = requests.get(link, headers=header)
        get_html = html.fromstring(request.text)
        time_news = get_html.xpath("//span[contains(@class, 'note__text')]/@datetime")
        data_pat = re.compile('\d+-\d+-\d+')
        time_pat = re.compile('\d+:\d+:\d+')
        data_news = re.findall(data_pat, time_news[0])
        time_news = re.findall(time_pat, time_news[0])
        time_f = data_news[0] + ' ' + time_news[0]
    except:
        time_format = "%Y-%m-%d %H:%M:%S"
        time_f = f"{datetime.now():{time_format}}"
    finally:
        return time_f


# Запрашиваем новости и выводим результаты

news_lenta = news_from_lenta()
if len(news_lenta) == 0:
    news_lenta = "Что-то пошло не так. Sorry..."

print(f'Новости с {main_link1}:\n{news_lenta}\n')

news_mail = news_from_mail()
if len(news_mail) == 0:
    news_mail = "Что-то пошло не так. Sorry..."
print(f'Новости с {main_link2}:\n{news_mail}')

