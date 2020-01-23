from django.shortcuts import render
from weather.models import Cities
from weather.models import Weather
from django.db.models import Avg, Max, Min, Count
from datetime import date, datetime, timedelta

def index(request):
    temp_start = request.GET.get('start_date')
    temp_end = request.GET.get('end_date')
    start_date = date.today()-timedelta(days=1)
    end_date = date.today()
    if temp_start:
        start_date = datetime.strptime(temp_start, '%d-%m-%Y').date()
    if temp_end:
        end_date = datetime.strptime(temp_end, '%d-%m-%Y').date()
    delta = timedelta(730)
    time_period = end_date-start_date

    cityname = request.GET.get('city')
    cities = Cities.objects.all()
    percipitation = Weather.objects.filter(date__gte=start_date, date__lte=end_date, precipitation__isnull=False,
                                           city__city_name=cityname).values('date').annotate(precipitation_with=Count('precipitation')).aggregate(days_c=Count('date'))

    percipitation_max_freq = Weather.objects.filter(date__gte=start_date, date__lte=end_date, precipitation__isnull=False,
                                                city__city_name=cityname).values('precipitation__precipitation').annotate(p_freq=Count('precipitation')).order_by('-p_freq')[:2]


    percent = (percipitation['days_c']/time_period.days)*100

    weather = Weather.objects.filter(date__gte=start_date, date__lte=end_date, city__city_name=cityname).aggregate(
        average_t=Avg('temperature'), max_t=Max('temperature'), min_t=Min('temperature'), average_speed=Avg('wind_speed'))

    weather_by_year = Weather.objects.filter(date__gte=start_date, date__lte=end_date, city__city_name=cityname).extra(select={'year': "EXTRACT(year FROM date)"}).values('year').annotate(
        average_t=Avg('temperature'), max_t=Max('temperature'), min_t=Min('temperature'), average_speed=Avg('wind_speed')).order_by('year')

    wind_speed = Weather.objects.filter(date__gte=start_date, date__lte=end_date, city__city_name=cityname).aggregate(
        average_speed=Avg('wind_speed'))

    wind = Weather.objects.filter(date__gte=start_date, date__lte=end_date,
                                  city__city_name=cityname).values('wind_direction__wind_full_name').annotate(w_freq=Count('wind_direction')).order_by('-w_freq')[:1]

    return render(request, 'index.html', {'weather': weather, 'weather_years': weather_by_year, 'time_period': time_period.days,
                                          'percipitation': percipitation, 'cities': cities,
                                          'percipitation_freq': percipitation_max_freq,
                                          'percent': percent, 'start_date': start_date, 'end_date':end_date,
                                          'get_city': cityname, 'wind_speed':wind_speed, 'wind':wind, 'delta': delta, 'time': time_period})
