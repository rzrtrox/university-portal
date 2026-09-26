import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campusconnect.settings")
import django
django.setup()

from django.contrib.auth.models import User
from base.models import Profile, Story

print("Seeding realistic Campus Stories data...")

# 1. Clean existing stories so we have a clean, pristine dataset
deleted_count = Story.objects.all().delete()[0]
print(f"Cleared {deleted_count} old stories.")

# 2. Ensure realistic student profiles exist
students = [
    {
        "username": "riya_sharma",
        "email": "riya@campus.edu",
        "first_name": "Riya",
        "last_name": "Sharma",
        "program": "Computer Science",
        "semester": 4,
        "profile_pic": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&auto=format&fit=crop&q=80",
    },
    {
        "username": "aman_patel",
        "email": "aman@campus.edu",
        "first_name": "Aman",
        "last_name": "Patel",
        "program": "Robotics & AI",
        "semester": 6,
        "profile_pic": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80",
    },
    {
        "username": "neha_verma",
        "email": "neha@campus.edu",
        "first_name": "Neha",
        "last_name": "Verma",
        "program": "Design & Media",
        "semester": 2,
        "profile_pic": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=200&auto=format&fit=crop&q=80",
    },
]

created_profiles = []
for s in students:
    user, created = User.objects.get_or_create(
        username=s["username"],
        defaults={"email": s["email"], "first_name": s["first_name"], "last_name": s["last_name"]}
    )
    if created:
        user.set_password("campus123")
        user.save()

    prof, p_created = Profile.objects.get_or_create(
        username=user,
        defaults={
            "f_name": s["first_name"],
            "l_name": s["last_name"],
            "program": s["program"],
            "semester": s["semester"],
            "gender": "F" if "Sharma" in s["last_name"] or "Verma" in s["last_name"] else "M",
            "relationship_status": "single",
            "bio": f"Passionate about {s['program']} • Class of 2026",
            "profile_pic": s["profile_pic"],
        }
    )
    if not p_created and not prof.profile_pic:
        prof.profile_pic = s["profile_pic"]
        prof.save()
    created_profiles.append(prof)

# Also fetch all existing profiles
all_profiles = list(Profile.objects.all())
print(f"Total available student profiles: {len(all_profiles)}")

# 3. Seed multi-story slides for authors
stories_blueprint = [
    {
        "username": "riya_sharma",
        "slides": [
            {
                "image": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Morning study group at the engineering library 📚☕",
            },
            {
                "image": None,
                "video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "caption": "Campus fest rehearsals are officially underway! 🎶🔥",
            },
            {
                "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Golden hour over the main quad ✨",
            },
        ],
    },
    {
        "username": "aman_patel",
        "slides": [
            {
                "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Robotics lab testing autonomous rover navigation 🤖🛠️",
            },
            {
                "image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Hackathon team locked in for the next 24 hours 💻⚡",
            },
        ],
    },
    {
        "username": "neha_verma",
        "slides": [
            {
                "image": "https://images.unsplash.com/photo-1460518451285-97b6aa326961?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Annual art & design showcase in the north hall 🎨🖼️",
            },
            {
                "image": None,
                "video": "https://www.w3schools.com/html/mov_bbb.mp4",
                "caption": "Animation club short film teaser! 🎬🐰",
            },
        ],
    },
]

# If existing users like atharv, codespace, or rzrtrox exist, give one of them stories too
existing_author = Profile.objects.filter(username__username__in=["atharv", "codespace", "rzrtrox"]).first()
if existing_author:
    stories_blueprint.append({
        "username": existing_author.username.username,
        "slides": [
            {
                "image": "https://images.unsplash.com/photo-1519452635265-7b1fbfd1e4e0?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Fresh semester vibes on campus! Ready for exams 🚀",
            },
            {
                "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1080&auto=format&fit=crop&q=80",
                "video": None,
                "caption": "Graduation day countdown is real 🎓✨",
            }
        ]
    })

total_stories_created = 0
for author_data in stories_blueprint:
    author_prof = Profile.objects.filter(username__username=author_data["username"]).first()
    if not author_prof:
        continue

    for s_idx, slide in enumerate(author_data["slides"]):
        story = Story.objects.create(
            profile=author_prof,
            image=slide["image"],
            video=slide["video"],
            caption=slide["caption"],
        )
        total_stories_created += 1

        # Simulate viewers (other student profiles)
        other_profs = [p for p in all_profiles if p.id != author_prof.id]
        if other_profs:
            viewers_to_add = other_profs[:min(4, len(other_profs))]
            story.viewers.add(*viewers_to_add)

            likers_to_add = viewers_to_add[:min(2, len(viewers_to_add))]
            story.likes.add(*likers_to_add)

print(f"Successfully created {total_stories_created} dynamic stories across {len(stories_blueprint)} authors with real viewers and likes!")
