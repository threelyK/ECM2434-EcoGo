from django.urls import path

from . import views

# These are the URLs which direct the user to each page in our website.
urlpatterns = [
    path('announcements', views.announcement_list, name="announcement_list"), # takes user to all the announcements
    path('announcement/<slug:slug>/', views.announcement, name="announcement"),
]