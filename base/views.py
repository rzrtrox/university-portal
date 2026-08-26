from django.shortcuts import redirect, render,get_object_or_404
from .models import Profile
from django.contrib.auth.models import User



def index(request):
    return render(request, "index.html")

def login(request):
    print("Login request method:")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Login attempt for user:", username)
        user = User.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            # Successful login
            print("Login successful for user:", username)
            return redirect("home")
        else:
            # Invalid credentials
            error_message = "Invalid username or password."
            return render(request, "authentication/login.html", {"error_message": error_message})

    return render(request, "authentication/login.html")


def create_account(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        semester = request.POST.get("semester")
        # email = request.POST.get("email")
        password = request.POST.get("password")
        errors = {}

        if User.objects.filter(username=username).exists():
           print("Username already exists.")
           errors["username"] = "Username already exists."

        if errors:
            return render(
                request,
                "authentication/create_ac.html",
                {
                    "errors": errors,
                    "username": username,
                }
            )

        user = User.objects.create_user(username=username, password=password)
        user.save()
        profile = Profile(username=user, semester=semester, f_name=first_name, l_name=last_name,)
        profile.save()

        return redirect("login")
    print("Creating account...")
    return render(request, "authentication/create_ac.html")

def home(request):
    print("Username",request.user.username)
    username = request.user.username
    print("Username",request.user.username)
    username = request.user.username
    profile_obj = get_object_or_404(Profile, username__username=username)
    program = profile_obj.program + " • Semester " + str(profile_obj.semester)
    return render(request, "home/index.html",{"username":username,"profile":profile_obj,"program":program})


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


def discover_people(request):
    return render(request, "discover/index.html")
