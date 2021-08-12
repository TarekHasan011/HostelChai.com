import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()

from django.conf import settings


def add_dictionary(dict_1, dict_2):
    for key in dict_2.keys():
        dict_1[key] = dict_2[key]
    return dict_1


def all_thana():
    file = open(f'{os.path.join(settings.BASE_DIR, "text_files")}/thanas.txt')
    thanas = [t.split('\n')[0] for t in file.readlines()]
    file.close()
    return thanas


def all_institutes():
    file = open(f'{os.path.join(settings.BASE_DIR, "text_files")}/institution_names.txt')
    institutes = [t.split('\n')[0] for t in file.readlines()]
    file.close()
    return institutes
