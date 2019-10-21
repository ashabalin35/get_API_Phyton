from pprint import pprint
from pymongo import MongoClient
from bs4 import BeautifulSoup as Bs
import requests
import re

client = MongoClient('localhost', 27017)
db = client['BIGDATA']
vac = db.vac

superjob = []  # Заявляем список для данных с сайта https://www.superjob.ru
hh = []  # Заявляем список для данных с сайта https://hh.ru

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

main_link1 = 'https://www.superjob.ru'

main_link2 = 'https://hh.ru'

# Запрашиваем данные для поиска
vacancy = input('По какому слову будем запрашивать информацию о вакансиях и сохранять в базу?\n')
pages = int(input('Сколько страниц будем обрабатывать?\n'))


# Функция получения данных с hh.ru
def hh_get():
    html = requests.get(main_link2 + '/search/vacancy?st=searchVacancy&text=' + vacancy,
                        headers=headers).text  # формируем первую ссылку для hh.ru
    for i in range(pages):
        parsed_html = Bs(html, 'lxml')
        vacancy_list = parsed_html.findAll('div', {'class': 'vacancy-serp-item'})

        for vac in vacancy_list:
            hh_data = {}

            # Название вакансии
            vacancy_name = vac.find('span', {'class': 'g-user-content'}).findChild().getText()

            # Ссылка на вакансию
            vacancy_link = vac.find('span', {'class': 'g-user-content'}).findChild()['href']

            # Зарплата
            vacancy_salary = vac.find('div', {'class': 'vacancy-serp-item__compensation'})
            if not vacancy_salary:
                salary = {'min': 0, 'max': 0, 'type': 'Не указано'}
            else:
                salary_data = re.findall('(\d+[\s\d]*)', vacancy_salary.getText())
                salary_type = re.findall('([А-яA-z]{3}\.*)', vacancy_salary.getText())
                if not salary_type:
                    salary_type = 'руб.'
                if len(salary_data) > 1:
                    salary = {'min': int(salary_data[0].replace('\xa0', '')),
                              'max': int(salary_data[1].replace('\xa0', '')), 'type': salary_type[0]}
                else:
                    salary = {'min': int(salary_data[0].replace('\xa0', '')), 'max': 0, 'type': salary_type[0]}

            # Название компании
            company = vac.find('div', {'class': 'vacancy-serp-item__meta-info'}).findChild()
            if not company:
                company = 'Не указано'
            else:
                company = company.getText()

            # Должностные обязанности и требования к кандидату
            job_responsibility = vac.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
            if not job_responsibility:
                job_responsibility = 'Не указано'
            else:
                job_responsibility = job_responsibility.getText()

            job_requirement = vac.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
            if not job_requirement:
                job_requirement = 'Не указано'
            else:
                job_requirement = job_requirement.getText()

            # Собираем и складываем
            hh_data['vacancy_from'] = main_link2
            hh_data['vacancy_name'] = vacancy_name
            hh_data['company'] = company
            hh_data['job_responsibility'] = job_responsibility
            hh_data['job_requirement'] = job_requirement
            hh_data['salary'] = salary
            hh_data['vacancy_link'] = vacancy_link
            hh.append(hh_data)

        # получаем ссылку на следующую страницу
        link_next = parsed_html.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if not link_next:
            if i + 1 < pages:
                print(f'На сайте "{main_link2}" доступно лишь {i + 1} страниц(ы) информации из желаемых {pages}\n')
            break
        else:
            link_next = link_next['href']
            new_link = main_link2 + link_next
            html = requests.get(new_link, headers=headers).text  # формируем ссылку на следующую страницу
    return hh


# Функция получения данных с superjob.ru
def superjob_get():
    html = requests.get(main_link1 + '/vacancy/search/?keywords=' + vacancy,
                        headers=headers).text  # формируем первую ссылку для superjob

    for i in range(pages):

        parsed_html = Bs(html, 'lxml')
        vacancy_list = parsed_html.findAll('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})

        for vac in vacancy_list:
            superjob_data = {}
            main_info = vac.find('div', {'class': '_2g1F-'}).findChild()

            # Название вакансии
            vacancy_name = main_info.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()

            # Ссылка на вакансию
            vacancy_link = main_link1 + main_info.find('a')['href']

            # Зарплата
            vacancy_salary = main_info.find('span', {
                'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
            if not vacancy_salary or vacancy_salary.getText() == 'По договорённости':
                salary = {'min': 0, 'max': 0, 'type': 'Не указано'}
            else:
                salary_data = re.findall('[от\s]*(\d+\s\d+)', vacancy_salary.getText())
                if not salary_data:
                    salary = {'min': 0, 'max': 0, 'type': 'Не указано'}
                else:
                    if len(salary_data) > 1:
                        salary = {'min': int(salary_data[0].replace('\xa0', '')),
                                  'max': int(salary_data[1].replace('\xa0', '')), 'type': 'руб.'}
                    else:
                        salary = {'min': int(salary_data[0].replace('\xa0', '')), 'max': 0, 'type': 'руб.'}

            # Название компании
            company = main_info.find('span', {
                'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'})
            if not company:
                company = 'Не указано'
            else:
                company = company.getText()

            # Должностные обязанности и требования к кандидату
            job_res = main_info.findAll('span', {'class': '_3mfro _9fXTd _2JVkc _2VHxz'})  # .getText()
            if len(job_res) > 1:
                job_responsibility = job_res[0].getText()
                if 'Должностные обязанности:' in job_responsibility:
                    job_responsibility = re.findall('Должностные обязанности:\s(.+)', job_responsibility)[0]
                else:
                    job_responsibility = 'Не указано'
                job_requirement = job_res[1].getText()
                if 'Требования:' in job_requirement:
                    job_requirement = re.findall('Требования:\s(.+)', job_requirement)[0]
                else:
                    job_requirement = 'Не указано'
            elif len(job_res) == 1:
                job_responsibility = job_res[0].getText()
                if 'Должностные обязанности:' in job_responsibility:
                    job_responsibility = re.findall('Должностные обязанности:\s(.+)', job_responsibility)[0]
                else:
                    job_responsibility = 'Не указано'
                job_requirement = job_res[0].getText()
                if 'Требования:' in job_requirement:
                    job_requirement = re.findall('Требования:\s(.+)', job_requirement)[0]
                else:
                    job_requirement = 'Не указано'
            else:
                job_responsibility = 'Не указано'
                job_requirement = 'Не указано'

            # Собираем и складываем в MongoDB
            superjob_data['vacancy_from'] = main_link1
            superjob_data['vacancy_name'] = vacancy_name
            superjob_data['company'] = company
            superjob_data['job_responsibility'] = job_responsibility
            superjob_data['job_requirement'] = job_requirement
            superjob_data['salary'] = salary
            superjob_data['vacancy_link'] = vacancy_link
            superjob.append(superjob_data)

        # получаем ссылку на следующую страницу
        link_next = parsed_html.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})
        if not link_next:
            if i + 1 < pages:
                print(f'На сайте "{main_link1}" доступно лишь {i + 1} страниц(ы) информации из желаемых {pages}\n')
            break
        else:
            link_next = link_next['href']
            new_link = main_link1 + link_next
            html = requests.get(new_link, headers=headers).text  # формируем ссылку на следующую страницу
    return superjob


# функция для сохранения в базу
def to_mongodb(items):
    try:
        dubl = 0
        unic = 0
        for data in items:
            link1 = data['vacancy_link']
            x = 0
            objects = vac.find()
            for obj in objects:
                link2 = obj['vacancy_link']
                if link1 == link2:
                    x = 1
                    dubl += 1
            if x == 0:
                vac.insert_one(data)
                unic += 1
        if unic == 0:
            res = 'новых вакансий не обнаружено'
        else:
            res = f'записано {unic} новых вакансий. {dubl} - уже существуют в базе.'

    except:
        res = 'возникли проблемы при сохранении в MongoDB.\n'
    return res


# Получаем данные
hh_data = hh_get()
superjob_data = superjob_get()

# Сохраняем в базу
res = to_mongodb(hh_data)
print(f'При обработке данных hh.ru {res}')
res = to_mongodb(superjob_data)
print(f'При обработке данных superjob.ru {res}')


# Выводим вакансии из Базы по нужному уровню зарплаты
num = int(input('\nКакой уровень зарплаты интересует?: '))

# Выводим все. Обрабатывать разные валюты сейчас не будем.
objects = vac.find()
print('\nВозможно вам подойдут (без учета валюты):\n')
for o in objects:
    if (o['salary']['max'] > num) or (o['salary']['min'] != 0 and o['salary']['max'] == 0):
        if o['salary']['max'] != 0:
            s_max = f" до {o['salary']['max']}"
        else:
            s_max = ''
        print(f"{o['vacancy_name']}, зарплата от {o['salary']['min']}{s_max}, ссылка: {o['vacancy_link']}")
a = input('\nПоказать вакансии, где уровень зарплаты не указан? (yes, no)\n')
if a == 'yes':
    objects = vac.find({'salary.min': {'$eq': 0}})
    for i in objects:
        print(f"{i['vacancy_name']}, ссылка: {o['vacancy_link']}")
elif a == 'no':
    print('Как хотите :) Bye')
else:
    print('Ваш ответ непонят. Считаем что вы имели ввиду "no". Bye')