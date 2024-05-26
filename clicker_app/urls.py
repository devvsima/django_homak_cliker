# clicker_app/urls.py
from django.urls import path
from .views import click, upgrade, buy_bot, buy_character, leaderboard, signup_view, login_view, logout_view

urlpatterns = [
    path('click/', click, name='click'),
    path('upgrade/', upgrade, name='upgrade'),
    path('buy_bot/', buy_bot, name='buy_bot'),
    path('buy_character/', buy_character, name='buy_character'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
