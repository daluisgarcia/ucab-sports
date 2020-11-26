# food/urls.py
from django.conf.urls import url
from django.urls import path
from main.views import *

app_name='main'
urlpatterns = [
    path('', index, name='index'),
    path('posts/', ListaPosts.as_view(), name='lista_posts'),
    path('post/crear/', CrearPost.as_view(), name='crear_post'),
    path('torneos/', ListaTorneos.as_view(), name='lista_torneos'),
    path('torneo/crear/', CrearTorneo.as_view(), name='crear_torneo'),
]