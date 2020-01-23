from django.urls import path
from weather.views import index

app_name = 'weather'
urlpatterns = [
    path('', index, name='index')
]