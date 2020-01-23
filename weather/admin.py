from django.contrib import admin
from weather.models import Cities, Precipitation, Weather, Wind


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    pass

@admin.register(Precipitation)
class PrecipitationAdmin(admin.ModelAdmin):
    pass

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('date', 'temperature', 'city')
    list_filter = ('city',)
    date_hierarchy = 'date'


@admin.register(Wind)
class WindAdmin(admin.ModelAdmin):
    pass
# Register your models here.
