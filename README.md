# api_yamdb

### Описание проекта YaMDb:

Cбор отзывов пользователей на произведения (Книги, Фильмы, Музыка).

Позволяет делать запросы к моделям проекта: Произведения, Категории, Жанры, Отзывы, Комментарии.

Доступ через REST API.

Поддерживает методы GET, POST, PATCH, DELETE

Предоставляет данные в формате JSON

Документация доступна по URL-адресу: [127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

### В проекте предоставлена возможность:
   1. Вносить новые произведения и присваивать им жанр и категорию
   2. Создавать отзывы на произведения
   3. Выставлять оценку произведению от 1 до 10 (на основании оценок формируется рейтинг) 
   4. Комментировать и удалять свои комментарии

### Используемые технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/magicbuka/api_yamdb.git

Cоздать и активировать виртуальное окружение:

python -m venv venv

source venv/Scripts/activate

Установить зависимости из файла requirements.txt:

pip install -r requirements.txt

Выполнить миграции:

python manage.py migrate

Запустить проект:

python manage.py runserver

Заполнить базу данных тестовыми данными из файлов формата ".csv"

python manage.py importdata

### Разработчики проекта:
- [Baranova Anna](https://github.com/magicbuka)
- [Grachev Vladislav](https://github.com/grachevvladislav)
