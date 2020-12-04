# food/urls.py
from django.conf.urls import url
from django.urls import path
from main.views import *

app_name='main'
urlpatterns = [
    path('', index, name='index'),
    #Posts
    path('posts/', PostsList.as_view(), name='posts_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/create/', CreatePost.as_view(), name='create_post'),
    path('post/edit/<int:pk>/', UpdatePost.as_view(), name='update_post'),
    #Torneos
    path('torneos/', TorneosList.as_view(), name='torneos_list'),
    path('torneo/<int:pk>/', TorneoDetail.as_view(), name='torneo_detail'),
    path('torneo/create/', CreateTorneo.as_view(), name='create_torneo'),
    path('torneo/edit/<int:pk>/', UpdateTorneo.as_view(), name='update_torneo'),
    #Juegos
    path('juegos/', GamesList.as_view(), name='games_list')
]