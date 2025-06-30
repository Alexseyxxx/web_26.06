import argparse
import time

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--count", type=int)
    def generate(self, *args, **options):
        count = options.get('count')
        if not count:
            count = 100
        objs = []
        for i in range(count):
            objs.append(User(
                username=f"user_{i+1}",
                email="Ivan@mail.ru",
                password=make_password("qwe123!"),
                is_activate = True
            ))
            print(f'создал объект {i+1}')
        print('я работаю')
        User.objects.bulk_create(objs=objs, ignore_conflicts=True, batch_size= 500)


    def handle(self, *args, **options):
        print('Start Generate Users')
        start = time.perf_counter()
        self.generate(*args, **options)
        print('Users generated succssfully')
        end = time.perf_counter()
        print(f"Выполнено за {end-start:.4f} секунды")