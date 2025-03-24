from django.urls import path

from . import views

# These are the URLs which direct the user to each page in our website.
urlpatterns = [
    path('', views.landing, name="landing"),  # Takes the user to the initial page with login/register options
    path('register', views.register, name="register"),  # Takes the user to the register page
    path('login', views.user_login, name="login"),  # Takes the user to the login page
    path('homepage', views.homepage, name="homepage"),  # Takes the user to the home page if they are already logged in
    path('user-logout', views.user_logout, name="user-logout"),  # Logs the user out
    path("user/inventory", views.inventory, name="user-inventory"), # Takes the user to their inventory, and buy cards
    path('logout', views.user_logout, name="logout"),  # Logs the user out
    path('user/shop', views.shop, name="shop"),  # Takes the user to the shop page, and allows them to buy a card
    path('user/leaderboard', views.leaderboard, name="leaderboard"), # Creates the leaderboard 
]
