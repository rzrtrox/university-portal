from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("", views.home, name="home"),
    path("create-account", views.create_account, name="create_account"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/update/", views.update_profile, name="update_profile"),
    path("discover/", views.discover_people, name="discover_people"),
    path("clubs", views.clubs, name="clubs"),
    path("events", views.events, name="events"),

    # Post endpoints
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/", views.detailed_post, name="detailed_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/like/", views.toggle_post_like, name="toggle_post_like"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),

    # Comment endpoints
    path("comment/<int:comment_id>/like/", views.toggle_comment_like, name="toggle_comment_like"),
    path("comment/<int:comment_id>/reply/", views.add_reply, name="add_reply"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),

    # Story endpoints
    path("story/create/", views.create_story, name="create_story"),
    path("story/<int:story_id>/view/", views.mark_story_viewed, name="mark_story_viewed"),
    path("story/<int:story_id>/like/", views.toggle_story_like, name="toggle_story_like"),
    path("story/<int:story_id>/viewers/", views.story_viewers_list, name="story_viewers_list"),
    path("story/<int:story_id>/delete/", views.delete_story, name="delete_story"),
]