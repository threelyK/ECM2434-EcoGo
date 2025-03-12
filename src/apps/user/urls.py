from django.urls import path

from . import views

# These are the URLs which direct the user to each page in our website.
urlpatterns = [
    path('', views.landing, name="landing"),  # Takes the user to the initial page with login/register options
    path('register', views.register, name="register"),  # Takes the user to the register page
    path('login', views.user_login, name="login"),  # Takes the user to the login page
    path('homepage', views.homepage, name="homepage"),  # Takes the user to the home page if they are already logged in
    path('user-logout', views.user_logout, name="user-logout"),  # Logs the user out
    path("user/inventory", views.inventory, name="user-inventory"), # Takes the user to their inventory
    path("user/inventory/sellCard", views.sell_card, name="sell-card"), # Sells a specified user card
    path('logout', views.user_logout, name="logout"),  # Logs the user out
    path('user/leaderboard', views.leaderboard, name="leaderboard"), # Creates the leaderboard 
]
