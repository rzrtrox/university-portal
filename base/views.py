from django.shortcuts import render,get_object_or_404
from .models import Profile
def index(request):
    return render(request, "index.html")


def home(request):
    print("Username",request.user.username)
    username = request.user.username
    return render(request, "home/index.html",{"username":username})


def profile(request,username):
    profile_obj = Profile.objects.get(username__username=username)
    return render(request, "profile/index.html",{"profile":profile_obj})