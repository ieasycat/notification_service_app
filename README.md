# notification_service_app

Проект сервиса уведомлений

Использовался следующий стэк

```
- Celery
- Django
- django_celery_beat
- django_phonenumber_field
- Django Rest Framework
- drf-yasg
- psycopg2
- python-dotenv
- redis
```

## Установка и запуск(локально):

   - git@github.com:ieasycat/notification_service_app.git
   - source venv_name/bin/activate
   - pip install -r requirements.txt
   - python manage.py makemigrations
   - python manage.py migrate
   - python manage.py createsuperuser
   - python manage.py loaddata main_fixtures.json
   - python manage.py runserver
   - celery -A notification_service worker -l info
   - celery -A notification_service flower --port=5555

```
http://127.0.0.1:5555 -по этому адресу можно открыть flower
```

## Установка и запуск(docker-compose):

1. Добавить файл с переменными окружения(.env_docker) в корень проекта
2. Запустить командой:

```
   docker-compose up -d --build
```

## Описание методов и документация:

```
http://127.0.0.1:8000/docs/
```

### Дополнительно реализовано:

- подготовить docker-compose для запуска всех сервисов проекта одной командой(пункт №3)
- документация(пункт №5)
- администраторский Web UI (http://127.0.0.1:8000/admin/)(пункт №6)
- обработка ошибок удалённого сервера и создание статуса 'Error' сообщения с последующим созданием периодической задачи(пункт №9)
- реализована дополнительная возможность отправки уведомлений клиентам в зависимости от часового пояса клиента. Если время не соответствует необходимому диапазону, задача получает статус 'Wrong Time' и будет повторно запущена через 1 час(пункт №11)
