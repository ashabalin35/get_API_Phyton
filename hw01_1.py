import requests
import json
main_link = 'https://api.github.com/users/'
user_name = input('Введите имя пользователя GITHUB: ')
gets = requests.get(main_link+user_name+'/repos')
if gets.ok:
    data = json.loads(gets.text)
    with open('github.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
        print('Cохранили полученные данные в файл github.json\n')
    print(f'Смотрим список всех доступных репозиториев пользователя {user_name}:\n')
    for i in data:
        print(i['name'])

else:
    print('Неверное имя пользователя')