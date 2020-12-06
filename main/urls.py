# food/urls.py
from django.conf.urls import url
from django.urls import path
from main.views import *
from .views import IndexViews
from .views import PostViews
from .views import TournamentViews
from .views import StageViews

app_name='main'
urlpatterns = [
    path('', IndexViews.index, name='index'),
    #Posts
    path('posts/', PostViews.PostsList.as_view(), name='posts_list'),
    path('post/<int:pk>/', PostViews.PostDetail.as_view(), name='post_detail'),
    path('post/create/', PostViews.CreatePost.as_view(), name='create_post'),
    path('post/edit/<int:pk>/', PostViews.UpdatePost.as_view(), name='update_post'),
    #Torneos
    path('torneos/', TournamentViews.TorneosList.as_view(), name='torneos_list'),
    path('torneo/<int:pk>/', TournamentViews.TorneoDetail.as_view(), name='torneo_detail'),
    path('torneo/create/', TournamentViews.CreateTorneo.as_view(), name='create_torneo'),
    path('torneo/edit/<int:pk>/', TournamentViews.UpdateTorneo.as_view(), name='update_torneo'),
    #Statges
    path('fases/', StageViews.StageList.as_view(), name='stage_list'),
    path('fase/create', StageViews.CreateStage.as_view(), name='create_stage'),
    path('fase/<int:pk>', StageViews.StageDetail.as_view(), name='stage_detail'),
    path('fase/edit/<int:pk>', StageViews.UpdateStage.as_view(), name='update_stage'),
    path('fase/delete/<int:pk>', StageViews.DeleteStage.as_view(), name='delete_stage'),
    #Juegos
    path('juegos/', IndexViews.GamesList.as_view(), name='games_list')
]