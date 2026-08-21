from django.shortcuts import redirect, render,get_object_or_404
from .models import Profile
from django.contrib.auth.models import User



def index(request):
    return render(request, "index.html")


def home(request):
    print("Username",request.user.username)
    username = request.user.username
    return render(request, "home/index.html",{"username":username})


def profile(request,username):
    profile_obj = Profile.objects.get(username__username=username)
    return render(request, "profile/index.html",{"profile":profile_obj})


def update_profile(request, username):
    profile_obj = get_object_or_404(Profile, username__username=username)

    if request.method == "POST":
        # profile_obj.username.first_name = request.POST.get("fullname")
        profile_obj.username.username = request.POST.get("username")
        profile_obj.username.save()

        profile_obj.gender = request.POST.get("gender")
        profile_obj.relationship = request.POST.get("relationship")
        profile_obj.program = request.POST.get("program")
        profile_obj.birth_date = request.POST.get("birthdate")
        profile_obj.bio = request.POST.get("bio")

        if request.FILES.get("profile_pic"):
            profile_obj.profile_pic = request.FILES["profile_pic"]

        profile_obj.save()

        return redirect(
            "profile",
            username=profile_obj.username.username
        )

    return redirect(
        "profile",
        username=profile_obj.username.username
    )