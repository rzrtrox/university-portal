from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    GENDER = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    RELATIONSHIP = [
        ("single", "Single"),
        ("taken", "In Relationship"),
        ("complicated", "It's Complicated"),
        ("private", "Prefer not to say"),
    ]
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to="profile_pic/",blank=True, null=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    program = models.CharField(max_length=100, blank=True)
    semester = models.PositiveSmallIntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER
    )
    relationship_status = models.CharField(
        max_length=20,
        choices=RELATIONSHIP,
        default="private"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.username.username