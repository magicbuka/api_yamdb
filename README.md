# api_yamdb

### Описание проекта YaMDb:

Cбор отзывов пользователей на произведения (Книги, Фильмы, Музыка).

Позволяет делать запросы к моделям проекта: Произведения, Категории, Жанры, Отзывы, Комментарии.

Доступ через REST API.

Поддерживает методы GET, POST, PATCH, DELETE

Предоставляет данные в формате JSON

Документация доступна по URL-адресу: http://127.0.0.1:8000/redoc/

### В проекте предоставлена возможность:
   1. Вносить новые произведения и присваивать им жанр и категорию
   2. Создавать отзывы на произведения
   3. Выставлять оценку произведению от 1 до 10 (на основании оценок формируется рейтинг) 
   4. Комментировать и удалять свои комментарии

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/magicbuka/api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Разработчики проекта:
- Baranova Anna https://github.com/magicbuka
- Grachev Vladislav  https://github.com/grachevvladislav
