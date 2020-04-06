from requests import get, post, delete, put

print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'Работа',
                 'team_leader': 2,
                 'user_id': 1,
                 'work_size': '15',
                 'collaborators': '1, 2',
                 'is_finished': False}).json())  # Корректное добавление работы

print(post('http://localhost:5000/api/v2/jobs',
           json={'news': 'новость'}).json())  # Не корректное добавление работы: передан неправельный аргумент.

print(get('http://localhost:5000/api/v2/jobs').json())  # Корректный вывод всех работ.

print(get('http://localhost:5000/api/v2/job/1').json())  # Корректный вывод работы.

print(get('http://localhost:5000/api/v2/job/9999').json())  # Не корректный вывод: несуществующаяя работа.

print(delete('http://localhost:5000/api/v2/job/8').json())  # Корректное удаление работы.

print(delete('http://localhost:5000/api/v2/job/8').json())  # Не корректное удаление работы: Только что удаленная работа.
