# food/urls.py
from django.conf.urls import url
from django.urls import path
from main.views import *

app_name='main'
urlpatterns = [
    path('', index, name='index'),
    path('posts/', ListaPosts.as_view(), name='posts'),
]