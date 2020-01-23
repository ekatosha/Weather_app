from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Min, Count
from weather.models import Cities, Precipitation, Weather, Wind
import requests
import gzip
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        cur_date = date.today()
        date_aggr = Weather.objects.order_by('-date').first()
        if cur_date > date_aggr.date:
            start_date = date_aggr.date + timedelta(1)
            end_date = cur_date
            for city in Cities.objects.all():
                r = requests.get(city.url.format(start_date = start_date.strftime('%d.%m.%Y'), end_date = end_date.strftime('%d.%m.%Y')), allow_redirects=True)
                if r.status_code != 200:
                    continue
                open('test.gz', 'wb').write(r.content)
                with gzip.open('test.gz', 'rb') as f:
                    file_content = f.read()
                file = file_content.decode().split('\n')
                file[6] = file[6][:-1] + ';"space"\r'
                to_csv = ''.join(file[6:])
                with open('test.csv', 'w', newline='', encoding='utf-8') as f:
                    f.write(to_csv)
                update = pd.read_csv('test.csv', sep=';')
                del update['space']
                update['date'] = update.iloc[:, [0]].squeeze().str.split(' ').str.get(0)
                update['time'] = update.iloc[:, [0]].squeeze().str.split(' ').str.get(1)
                variable = []
                for index, row in update.iterrows():
                    row = row.dropna()
                    if 'RRR' not in row.keys() or row['RRR'] == 'Осадков нет' or row['RRR'] == 'Следы осадков':
                        precipitation_mm = None
                    else:
                        precipitation_mm = row['RRR']
                    if 'W1' not in row.keys() or not Precipitation.objects.filter(precipitation = row['W1']).exists():
                        precipitation = None
                    else:
                        precipitation = Precipitation.objects.filter(precipitation = row['W1']).first()
                    if 'DD' not in row.keys():
                        wind_direction = None
                    else:
                        wind_direction = Wind.objects.filter(wind_full_name = row['DD']).first()
                    if 'Ff' not in row.keys():
                        wind_speed = None
                    else:
                        wind_speed = row['Ff']
                    if 'T' not in row.keys():
                        temperature = None
                    else:
                        temperature = row['T']
                    dat = datetime.strptime(row['date'], '%d.%m.%Y').date()
                    variable.append(Weather(**{'date': dat, 'time': row['time'], 'city': city,
                                             'temperature': temperature,
                                             'wind_direction': wind_direction, 'wind_speed': wind_speed,
                                             'precipitation_mm': precipitation_mm, 'precipitation': precipitation}))
                Weather.objects.bulk_create(variable)



        #cities = Cities(country="New", city_name="Newest")
        #cities.save()
        #Cities.objects.create(country="New", city_name="Newest")
        #variable = []
        #for i in range(10):
            #variable.append(Cities(country=i, city_name=i))
        #Cities.objects.bulk_create(variable)

