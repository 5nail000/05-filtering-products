#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_agency.settings')
django.setup()

from django.db.models import Count
from property.models import Owner  # Импортируйте модель после инициализации Django

# Получим всех владельцев и подсчитайте количество связанных с ними квартир
owners = Owner.objects.annotate(num_flats=Count('flats'))

# только те, у которых больше одной квартиры
owners_with_multiple_flats = owners.filter(num_flats__gt=1)

# Вывод
for owner in owners_with_multiple_flats:
    print(f'Owner: {owner.full_name}, Number of flats: {owner.num_flats}')
