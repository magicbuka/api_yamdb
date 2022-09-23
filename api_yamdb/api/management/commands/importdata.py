from django.core.management.base import BaseCommand
import csv
import sqlite3


class Command(BaseCommand):
    help = 'Добавление в базу данных тестовых данных'

    def handle(self, *args, **options):
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()
        path = "static/data"
        file_name_dict = {
            'genre_title': {
                'db_name': 'genretitle',
                'instane_field': ['title', 'genre']
            },
            'users': {
                'db_name': 'user',
                'instane_field': []
            },
            'category': {
                'db_name': 'category',
                'instane_field': []
            },
            'comments': {
                'db_name': 'comment',
                'instane_field': ['author']
            },
            'genre': {
                'db_name': 'genre',
                'instane_field': []
            },
            'titles': {
                'db_name': 'title',
                'instane_field': ['category']
            },
            'review': {
                'db_name': 'review',
                'instane_field': ['title', 'author']
            },
        }
        SQL_FORM = (
            """INSERT INTO main.reviews_{}
            ({}) VALUES
            ('{}');"""
        )
        add_field = {
            'password': '',
            'is_staff': '0',
            'is_active': '1',
            'date_joined': '',
            'is_superuser': '0',
            'confirmation_code': ''
        }
        for name, db in file_name_dict.items():
            with open(f'{path}/{name}.csv', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                clean = {}
                for row in reader:
                    for key, value in row.items():
                        if key in db['instane_field']:
                            key += '_id'
                        clean[key] = value.replace("'", "''")
                    if db['db_name'] == "user":
                        clean.update(add_field)
                    try:
                        cursor.execute(
                            SQL_FORM.format(
                                db['db_name'],
                                ', '.join(clean.keys()),
                                "', '".join(clean.values())
                            )
                        )
                    except sqlite3.IntegrityError:
                        self.stdout.write('Запись уже существует!')
                    except sqlite3.OperationalError as e:
                        self.stdout.write(
                            f"Ошибка! {e} в строке:\n"
                            f"""'{"', '".join(clean.values())}'"""
                        )
            self.stdout.write(f'Файл {name}.csv импортирован!')
        sqlite_connection.commit()
        cursor.close()
