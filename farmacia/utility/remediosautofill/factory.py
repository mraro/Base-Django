# from inspect import signature
from random import randint
from faker import Faker

import re

import string as s
from random import SystemRandom as sr

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s
def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
def make_strong_string():
    print("".join(sr().choices(s.ascii_letters + s.punctuation, k=64)))

# print(signature(fake.random_number))

def make_medicine():
    return {
        # 'id': fake.random_number(digits=2, fix_len=True),
        'title': fake.sentence(nb_words=2),
        'description': fake.sentence(nb_words=12),
        # 'preparation_time': fake.random_number(digits=2, fix_len=True),
        # 'preparation_time_unit': 'Minutos',
        # 'servings': fake.random_number(digits=2, fix_len=True),
        # 'servings_unit': 'Porção',
        # 'price': (fake.random_number(digits=2, fix_len=True),fake.random_number(digits=2, fix_len=True)),
        'price': (fake.random_number(digits=2, fix_len=True)),
        # 'created_at': fake.date_time(),
        'author_data': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': {
            'name': fake.word()
        },
        # 'cover': {
        #     'url': 'https://loremflickr.com/%s/%s/' % rand_ratio(),
        # }
    }


def make_medicine_db():
    return {
        # 'id': fake.random_number(digits=2, fix_len=True),
        'title': fake.sentence(nb_words=2),
        'description': fake.sentence(nb_words=12),
        'slug': slugify(fake.sentence(nb_words=2)),
        # 'preparation_time': fake.random_number(digits=2, fix_len=True),
        # 'preparation_time_unit': 'Minutos',
        # 'servings': fake.random_number(digits=2, fix_len=True),
        # 'servings_unit': 'Porção',
        # 'price': (fake.random_number(digits=2, fix_len=True),fake.random_number(digits=2, fix_len=True)),
        'price': (fake.random_number(digits=2, fix_len=True)),
        'is_published':'True',
        # 'created_at': fake.date_time(),
        # 'author': {
        #     'first_name': fake.first_name(),
        #     'last_name': fake.last_name(),
        # },
        # 'category': {
        #     'name': fake.word()
        # },
        # 'cover': {
        #     'url': 'https://loremflickr.com/%s/%s/' % rand_ratio(),
        # }
    }


if __name__ == '__main__':
    from pprint import pprint


    make_strong_string()


    pprint(make_medicine_db())
