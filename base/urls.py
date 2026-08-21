from django.urls import path
from . import views

urlpatterns = [
    path("login",views.index, name="index"),
    path("",views.home, name="home"),
    path("profile/<str:username>/",views.profile, name="profile"),
    path("profile/<str:username>/update/", views.update_profile, name="update_profile"),

]