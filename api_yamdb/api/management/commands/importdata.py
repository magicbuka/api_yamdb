from django.core.management.base import BaseCommand
import csv, os

from reviews.models import User, Category, Genre, Comments, GenreTitle, Review, Title


class Command(BaseCommand):
    help = 'ррррррррррр'

    def handle(self, *args, **options):
        path = "static/data"
        filelist = []
        file_name_dict = {'category.csv': Category,
                          'comments.csv': Comments,
                          'genre.csv': Genre,
                          'genre_title.csv': GenreTitle,
                          'review.csv': Review,
                          'titles.csv': Title,
                          'users.csv': User
                          }
        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(file))

        for name in filelist:
            name = 'users.csv'
            with open(f'{path}/{name}', newline='') as csvfile:
                file = csv.reader(csvfile)
                for fow in file:
                    print(fow)
                # head_list = file[0].split(',')
                # body = file[1::]
                # for line in body:
                #     data_dict = dict(zip(head_list, line.split(r',\w')))
                #     print(name, data_dict)
                #     file_name_dict[name].objects.get_or_create(**data_dict)
                # self.stdout.write(f'File {name} was imported!')


