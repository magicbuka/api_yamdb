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
        for name, db in file_name_dict.items():
            with open(f'{path}/{name}.csv', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                clean = {}
                for row in reader:
                    for key, value in row.items():
                        if key in db['instane_field']:
                            key += '_id'

                        clean[key] = value.replace("'", "&qout")

                    try:
                        cursor.execute(
                            f"""INSERT INTO main.reviews_{db['db_name']}
                            ({', '.join(clean.keys())}) VALUES
                            ('{"', '".join(clean.values())}');"""
                        )
                    except sqlite3.IntegrityError:
                        self.stdout.write(f'Запись уже существует!')
                    except sqlite3.OperationalError as e:
                        self.stdout.write(
                            f"Ошибка! {e} в строке:\n"
                            f"""'{"', '".join(clean.values())}'"""
                        )
            self.stdout.write(f'Файл {name}.csv импортирован!')
        sqlite_connection.commit()
        cursor.close()
