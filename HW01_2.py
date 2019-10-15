import requests
import json
main_link='https://www.googleapis.com/youtube/v3/playlistItems'
param = 'part=snippet&playlistId=PLsQbj3-ckmTJwFoKd3Tv-aKWUD_ER2AH0'
key = 'AIzaSyDcsGuQhjNFbJCPK5ZO8Rh-gWEvwh0Yat0'

gets = requests.get(main_link+'?'+param+'&key='+key)

if gets.ok:
    print('Запрос прошел успешно, ответ получен...')
    data = json.loads(gets.text)
    with open('Playlist.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
        print('Cохранили полученные данные в файл Playlist.json\n')
    print('Посмотрим названия видео, полученых из плейлиста youtube:\n ')
    for i in data['items']:
        print(i['snippet']['title'])
else:
    print('Ошибка запроса... Sorry')