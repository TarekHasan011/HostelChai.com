import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()

from my_modules import classes
from django.db import connection
from django.conf import settings
from pathlib import Path
from django.conf import settings
from PIL import Image

cursor = connection.cursor()

base_dir = settings.BASE_DIR
text_files_dir = os.path.join(base_dir, 'text_files')
temp_files_dir = os.path.join(base_dir, 'temp_files')

file = open(f'{os.path.join(settings.BASE_DIR, "text_files")}/thanas.txt', 'r')

t = [t.split('\n')[0] for t in file.readlines()]

print(f'Total: {len(t)}')

[print(th) for th in t]