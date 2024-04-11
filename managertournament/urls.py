from django.urls import path
from . import views

app_name = 'managertournament'

urlpatterns = [
    path('', views.tournament_list, name='tournament_list'),
    path('tournament/<int:pk>/', views.tournament_detail, name='tournament_detail'),
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
    path('players/', views.player_list, name='player_list'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path('matches/', views.match_list, name='match_list'),
    path('match/<int:pk>/', views.match_detail, name='match_detail'),
    path('register/', views.registration_form, name='registration_form'),
    path('results/', views.result_form, name='result_form'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('tournament/create/', views.tournament_create, name='tournament_create'),
    path('tournament/<int:tournament_id>/create_match/', views.create_match, name='create_match'),
    path('match/<int:match_id>/update/', views.update_match, name='update_match'),
]
