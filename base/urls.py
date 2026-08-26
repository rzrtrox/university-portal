from django.urls import path
from . import views

urlpatterns = [
    path("login",views.login, name="login"),
    path("",views.home, name="home"),
    path("create-account", views.create_account, name="create_account"),
    path("profile/<str:username>/",views.profile, name="profile"),
    path("profile/<str:username>/update/", views.update_profile, name="update_profile"),
    path('discover/', views.discover_people, name="discover_people")

]