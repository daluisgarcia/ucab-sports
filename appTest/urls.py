# food/urls.py
from django.conf.urls import url
from django.urls import path
from appTest import views

app_name='appTest'
urlpatterns = [
    path('', views.index, name='index'),
]