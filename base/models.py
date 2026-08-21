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
    f_name = models.CharField(max_length=100, blank=True,null=True)
    l_name = models.CharField(max_length=100, blank=True,null=True)
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



class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="posts")
    caption = models.TextField(blank=True)

    image = models.ImageField(upload_to="posts/images/",blank=True,null=True)
    video = models.FileField(upload_to="posts/videos/",blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(Profile,related_name="liked_posts",blank=True)

    def __str__(self):
        return f"{self.profile.username.username} - {self.created_at}"

    

class Follow(models.Model):
    follower = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="following")
    following = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="followers")

    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("pending", "Pending"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="accepted"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow_relationship"
            ),
        ]

    def __str__(self):
        return f"{self.follower} follows {self.following}"