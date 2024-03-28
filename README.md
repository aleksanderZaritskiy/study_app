# Study_app - Техническое задание 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

## Использованные при реализации проекта технологии
 - Python
 - Django
 - djangorestframework
 - SQlite

## Установка проекта на локальный компьютер из репозитория 

### Для установки проекта необходимо выполнить следующие шаги:

### Базовая настройка:
 - Клонировать репозиторий `git clone <адрес вашего репозитория>`
 - Перейти в директорию с клонированным репозиторием
 - установить и развернуть виртуальное окружение
 - обновить pip и установить зависимости
 - выполнить команду python manage.py migrate из директории проекта
 - выполнить команду python manage.py runserver для запуска 
 - зарегистрировать пользователя и получить токен


---

### Инструкция по API:

1. Аутентификация и авторизация настроена на djoser + rest_framework.authtoken.
2. Основные эндпоинты для User:
    * http://127.0.0.1:8000/api/users/ (POST) - для регистрации
    * http://127.0.0.1:8000/api/auth/token/login/ (POST) - для получения токена
    Остальные эндпоинты в соответствии с документацией djoser
3. http://127.0.0.1:8000/api/course/ (POST, GET, PUT, PATCH, DELETE) - CRUD с объектами курса. Для каждого метода определены права доступа в permissions.py
4. http://127.0.0.1:8000/api/lesson/ (POST, GET, PUT, PATCH, DELETE) -CRUD с объектами урока. Для каждого метода определены права доступа в permissions.py
5. http://127.0.0.1:8000/api/get_pass/ (POST) - закрепляет за студентом доступ к курсу. В рамках тестирования доступен каждому авторизированному пользователю.
    При запросе к эндпоинту get_pass вызывается системный метод _formatted_group, который ребалансирует количетсво студентов между объектами Group.
6. http://127.0.0.1:8000/api/group/ (GET) - просмотр групп
7. http://127.0.0.1:8000/api/course/{id}/lesson/ - (GET) - просмотр уроков определенного курса, если у студента есть доступ к нему.
---
