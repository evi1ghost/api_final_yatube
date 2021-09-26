# Yatube API
**_Учебный проект_**

### Краткое описание:
API для социальной сети, в которой пользователи могут публиковать записи/сообщения и просматривать сообщению других пользователей. Реализованы механизм комментариев к записям, возможность подписка на публикации интересующий авторов, регистрация пользователей.
Для аутентификации используется JWT-токен.
В проекте использованы следующие инструменты:
_Python3, Django, DjangoORM, DjangoREST Framework, SQLite_

## Подготовка проекта
### Создать и активировать виртуальное окружение, установить зависимости:
```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Создать базу и применить миграции:
Из директории /project_dir/yatube_api/ выполнить:
```sh
python manage.py migrate
```

## Создание суперпользователя:
Выполнить комманду и следвать инструкциям:
```sh
python manage.py createsuperuser
```
После создания супепользователя можно использовать данные учетной записи для страницы администрирования - http://127.0.0.1:8000/admin/

## Запустить проект:
```sh
python manage.py runserver
```

**Документация доступкна по url: http://127.0.0.1:8000/redoc/**
