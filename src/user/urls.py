from django.urls import path

from . import views

urlpatterns = [

    path('', views.landing, name=""),

    path('register', views.register, name="register"),

    path('login', views.login, name="login"),

    path('home', views.homepage, name="home"),

    path('user-logout', views.user_logout, name="user-logout")
    
]