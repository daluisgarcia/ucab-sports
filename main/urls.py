# food/urls.py
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from main.views import *
from .views import IndexViews, PostViews,TournamentViews, GameViews, StageViews, RoleViews, InscriptionViews, PermissionViews


app_name='main'
urlpatterns = [
    
    path('', IndexViews.index, name='index'),
    
    #Posts
    path('post/create/', PostViews.CreatePost.as_view(), name='create_post'),
    path('posts/', PostViews.PostsList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostViews.PostDetail.as_view(), name='post_detail'),
    path('post/edit/<int:pk>/', PostViews.UpdatePost.as_view(), name='update_post'),
    path('post/delete/<int:pk>/', PostViews.DeletePost.as_view(), name='delete_post'),
    
    #Tournaments
    path('torneo/create/', TournamentViews.CreateTournament.as_view(), name='create_tournament'),
    #Asociar fases al torneo
    path('torneo/<int:pk>/create/', TournamentViews.createStageTournament, name='create_stage_tournament'),
    path('torneos/', TournamentViews.TournamentList.as_view(), name='tournament_list'),
    path('torneo/<int:pk>/', TournamentViews.tournamentInfo, name='tournament_detail'),
    path('torneo/edit/<int:pk>/', TournamentViews.UpdateTournament.as_view(), name='update_tournament'),
    path('torneo/delete/<int:pk>/', TournamentViews.DeleteTournament.as_view(), name='delete_tournament'),

    #Stages
    path('fases/', StageViews.StageList.as_view(), name='stage_list'),
    path('fase/create', StageViews.CreateStage.as_view(), name='create_stage'),
    path('fase/<int:pk>', StageViews.StageDetail.as_view(), name='stage_detail'),
    path('fase/edit/<int:pk>', StageViews.UpdateStage.as_view(), name='update_stage'),
    path('fase/delete/<int:pk>', StageViews.DeleteStage.as_view(), name='delete_stage'),
    
    #Games
    path('index/juegos/', IndexViews.GamesList.as_view(), name='games_list'),

    path('juego/create/', GameViews.CreateGame.as_view(), name='create_game'),
    path('juegos/', GameViews.GamesList.as_view(), name='game_list'),
    path('juego/edit/<int:pk>/', GameViews.UpdateGame.as_view(), name='update_game'),
    path('juego/delete/<int:pk>/', GameViews.DeleteGame.as_view(), name='delete_game'),

    #Roles
    path('rol/create/', RoleViews.CreateRole.as_view(), name='create_role'),
    path('roles/', RoleViews.RolesList.as_view(), name='role_list'),
    path('rol/edit/<int:pk>/', RoleViews.UpdateRole.as_view(), name='update_role'),

    #Permission
    path('permiso/create/', PermissionViews.CreatePermission.as_view(), name='create_permission'),
    path('permisos/', PermissionViews.PermissionList.as_view(), name='permission_list'),
    path('permiso/edit/<int:pk>/', PermissionViews.UpdatePermission.as_view(), name='update_permission'),
    
    #Preinscription
    path('inscripcion/<int:pk_torneo>/create/', InscriptionViews.createRegisterTeam, name='create_inscription'),
    path('inscripciones/pendientes/', InscriptionViews.preinscriptionList, name='inscription_list'),
    path('inscripcion/<int:pk>/', InscriptionViews.preinscriptionDetail, name='inscription_detail'),
    #Aprobar inscripción
    path('inscripciones/equipo/<int:pk_team>/torneo/<int:pk_tour>', InscriptionViews.approveInscription, name='approve_inscription'),
    #Anular inscripción
    path('inscripciones/anular/equipo/<int:pk_team>/torneo/<int:pk_tour>', InscriptionViews.failInscription, name='fail_inscription'),

    #Histórico de equipos por torneo
    path('equipos/', InscriptionViews.inscriptionList, name='team_list'),
    path('equipo/<int:pk>/', InscriptionViews.inscriptionDetail, name='team_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()