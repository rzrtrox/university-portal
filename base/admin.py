from django.contrib import admin
from .models import Profile, Post, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "program", "semester", "gender", "relationship_status", "created_at")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("profile", "caption", "created_at")

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")