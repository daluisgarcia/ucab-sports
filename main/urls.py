# food/urls.py
from django.conf.urls import url
from django.urls import path
from main import views

app_name='main'
urlpatterns = [
    path('', views.index, name='index'),
]