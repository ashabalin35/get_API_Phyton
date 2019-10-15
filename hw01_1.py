import requests
import json
main_link = 'https://api.github.com/users/'
user_name = input('Введите имя пользователя GITHUB: ')
gets = requests.get(main_link+user_name+'/repos')
if gets.ok:
    data = json.loads(gets.text)
    print(f'Список всех доступных репозиториев пользователя {user_name}:\n')
    for i in data:
        print(i['name'])
else:
    print('Неверное имя пользователя')