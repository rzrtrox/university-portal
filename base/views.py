from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile, Post, Comment, Story
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# ---------- HELPERS ----------
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.db.models import Count, Prefetch
import json
# xqc4FNpGdP3BHlt4

def _profile(user):
    """Return Profile for logged-in user, else None."""
    if not user.is_authenticated:
        return None
    return Profile.objects.filter(username=user).first()


def _avatar(profile):
    """Return avatar URL from whatever field your Profile has."""
    for attr in ("avatar", "image", "profile_pic", "profile_image"):
        f = getattr(profile, attr, None)
        if f:
            try:
                url_str = str(f)
                if url_str.startswith("http://") or url_str.startswith("https://"):
                    return url_str
                return f.url
            except Exception:
                return ""
    return ""


def _username(profile):
    """Return username string from profile."""
    u = getattr(profile, "username", None)
    # Profile.username is a User (based on your __str__) OR a CharField
    return getattr(u, "username", str(u)) if u else "unknown"



def index(request):
    return render(request, "index.html")

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Login attempt for user:", username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            print("Login successful for user:", username)

            return redirect("home")

        else:
            error_message = "Invalid username or password."
            return render(
                request,
                "authentication/login.html",
                {"error_message": error_message}
            )

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
    if not request.user.is_authenticated:
        return redirect("login")
    username = request.user.username
    profile_obj = get_object_or_404(Profile, username__username=username)
    program = profile_obj.program + " • Semester " + str(profile_obj.semester)

    category_filter = request.GET.get("category", "").strip()
    posts_qs = (
        Post.objects.select_related("profile__username")
        .prefetch_related("likes", "comments")
        .annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count("comments", distinct=True),
        )
        .order_by("-created_at")
    )
    if category_filter and category_filter != "all":
        posts_qs = posts_qs.filter(category=category_filter)

    liked_post_ids = set(profile_obj.liked_posts.values_list("id", flat=True))

    # Active 24-hour stories
    cutoff = timezone.now() - timedelta(hours=24)
    active_stories = (
        Story.objects.filter(created_at__gte=cutoff)
        .select_related("profile__username")
        .prefetch_related("viewers", "likes")
        .order_by("created_at")
    )

    grouped = {}
    for s in active_stories:
        grouped.setdefault(s.profile_id, []).append(s)

    stories_groups = []
    my_stories = []
    for p_id, s_list in grouped.items():
        p = s_list[0].profile
        serialized_list = [_serialize_story(s, profile_obj) for s in s_list]
        has_unseen = any(not s["viewed_by_me"] for s in serialized_list)
        group_item = {
            "profile_id": p.id,
            "username": _username(p),
            "name": f"{getattr(p, 'f_name', '')} {getattr(p, 'l_name', '')}".strip() or _username(p),
            "avatar": _avatar(p),
            "has_unseen": has_unseen,
            "is_me": p.id == profile_obj.id,
            "stories": serialized_list,
        }
        if p.id == profile_obj.id:
            my_stories = serialized_list
            stories_groups.insert(0, group_item)
        else:
            stories_groups.append(group_item)

    my_group = [g for g in stories_groups if g["is_me"]]
    other_groups = [g for g in stories_groups if not g["is_me"]]
    other_groups.sort(key=lambda g: not g["has_unseen"])
    stories_groups = my_group + other_groups
    stories_data_json = json.dumps(stories_groups)

    return render(
        request,
        "home/index.html",
        {
            "username": username,
            "profile": profile_obj,
            "program": program,
            "post": posts_qs,
            "liked_post_ids": liked_post_ids,
            "categories": Post.CATEGORY_CHOICES,
            "active_category": category_filter or "all",
            "stories_groups": stories_groups,
            "stories_data_json": stories_data_json,
            "my_stories": my_stories,
            "has_my_stories": bool(my_stories),
        },
    )



def profile(request,username):
    profile_obj = Profile.objects.get(username__username=username)
    user_posts = Post.objects.filter(profile=profile_obj)
    current_user = request.user.username
    program = profile_obj.program + " • Semester " + str(profile_obj.semester)
    return render(request, "profile/index.html",{"profile":profile_obj, "user_post":user_posts,"username":request.user.username,"program":program,"current_user":current_user})


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
    username = request.user.username
    profile_obj = get_object_or_404(Profile, username__username=username)
    program = profile_obj.program + " • Semester " + str(profile_obj.semester)
    return render(request, "discover/index.html",{"username":username,"profile":profile_obj,"program":program})


def clubs(request):
    username = request.user.username
    profile_obj = get_object_or_404(Profile, username__username=username)
    program = profile_obj.program + " • Semester " + str(profile_obj.semester)
    return render(request, "clubs/index.html" ,{"username":username,"profile":profile_obj,"program":program})


def events(request):
    username = request.user.username
    profile_obj = get_object_or_404(Profile, username__username=username)
    program = profile_obj.program + " • Semester " + str(profile_obj.semester)
    return render(request, "events/index.html" ,{"username":username,"profile":profile_obj,"program":program})


# def detailed_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     return render(request, "home/detailed_post.html", {"post": post})
def _serialize_comment(c, viewer):
    reply_to = None
    if c.parent_id:
        reply_to = _username(c.parent.author)

    is_staff = bool(viewer and hasattr(viewer.username, "is_staff") and viewer.username.is_staff)
    can_delete = bool(
        viewer
        and (
            viewer.id == c.author_id
            or viewer.id == c.post.profile_id
            or is_staff
        )
    )

    return {
        "id": c.id,
        "user": _username(c.author),
        "replyTo": reply_to,
        "handle": "@" + _username(c.author),
        "avatar": _avatar(c.author),
        "time": timesince(c.created_at) + " ago",
        "timestamp": int(c.created_at.timestamp() * 1000),
        "text": c.content,
        "likes": c.likes.count(),
        "userLiked": bool(viewer and c.likes.filter(id=viewer.id).exists()),
        "can_delete": can_delete,
        "replies": [_serialize_comment(r, viewer) for r in c.replies.all()],
    }


def _serialize_story(story, viewer):
    p = story.profile
    p_username = _username(p)
    name = f"{getattr(p, 'f_name', '')} {getattr(p, 'l_name', '')}".strip() or p_username
    is_staff = bool(viewer and hasattr(viewer.username, "is_staff") and viewer.username.is_staff)
    can_del = bool(viewer and (viewer.id == p.id or is_staff))
    viewed = bool(viewer and story.viewers.filter(id=viewer.id).exists())
    likes_cnt = story.likes.count()
    liked = bool(viewer and story.likes.filter(id=viewer.id).exists())

    media_url = ""
    media_type = "image"
    if story.video:
        try:
            v_str = str(story.video)
            if v_str.startswith("http://") or v_str.startswith("https://"):
                media_url = v_str
            else:
                media_url = story.video.url
            media_type = "video"
        except Exception:
            pass
    elif story.image:
        try:
            i_str = str(story.image)
            if i_str.startswith("http://") or i_str.startswith("https://"):
                media_url = i_str
            else:
                media_url = story.image.url
            media_type = "image"
        except Exception:
            pass

    return {
        "id": story.id,
        "profile_id": p.id,
        "username": p_username,
        "name": name,
        "avatar": _avatar(p),
        "caption": story.caption or "",
        "media_url": media_url,
        "media_type": media_type,
        "viewers_count": story.viewers.count(),
        "viewed_by_me": viewed,
        "likes_count": likes_cnt,
        "liked_by_me": liked,
        "can_delete": can_del,
        "time": timesince(story.created_at) + " ago",
        "created_at_ts": int(story.created_at.timestamp()),
    }


# ---------- AJAX & POST ENDPOINTS ----------
@require_POST
def create_post(request):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)

    caption = (request.POST.get("caption") or "").strip()
    category = request.POST.get("category") or "general"
    image = request.FILES.get("image")
    video = request.FILES.get("video")

    valid_categories = [c[0] for c in Post.CATEGORY_CHOICES]
    if category not in valid_categories:
        category = "general"

    if not caption and not image and not video:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": "Post cannot be empty."}, status=400)
        return redirect("home")

    post = Post.objects.create(
        profile=viewer,
        caption=caption,
        category=category,
        image=image,
        video=video,
    )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": True, "post_id": post.id})
    return redirect("home")


@require_POST
def delete_post(request, post_id):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)
    post = get_object_or_404(Post, id=post_id)
    is_staff = bool(hasattr(viewer.username, "is_staff") and viewer.username.is_staff)
    if post.profile_id != viewer.id and not is_staff:
        return JsonResponse({"error": "permission_denied"}, status=403)
    post.delete()
    return JsonResponse({"success": True})


@require_POST
def toggle_post_like(request, post_id):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=viewer.id).exists():
        post.likes.remove(viewer)
        liked = False
    else:
        post.likes.add(viewer)
        liked = True
    return JsonResponse({"liked": liked, "count": post.likes.count()})


@require_POST
def toggle_comment_like(request, comment_id):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.likes.filter(id=viewer.id).exists():
        comment.likes.remove(viewer)
        liked = False
    else:
        comment.likes.add(viewer)
        liked = True
    return JsonResponse({"liked": liked, "count": comment.likes.count()})


@require_POST
def add_comment(request, post_id):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)
    post = get_object_or_404(Post, id=post_id)
    content = (request.POST.get("content") or "").strip()
    if not content:
        return JsonResponse({"error": "empty"}, status=400)
    c = Comment.objects.create(post=post, author=viewer, content=content)
    return JsonResponse({
        "comment": _serialize_comment(c, viewer),
        "total_comment_count": post.comments.count(),
    })


@require_POST
def add_reply(request, comment_id):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)
    target = get_object_or_404(Comment.objects.select_related("author", "parent", "post"), id=comment_id)
    content = (request.POST.get("content") or "").strip()
    if not content:
        return JsonResponse({"error": "empty"}, status=400)

    # Single-level threading: attach to root parent comment
    if target.parent_id:
        root_parent = target.parent
        target_username = _username(target.author)
    else:
        root_parent = target
        target_username = _username(target.author)

    r = Comment.objects.create(
        post=root_parent.post, author=viewer, parent=root_parent, content=content
    )
    serialized = _serialize_comment(r, viewer)
    serialized["replyTo"] = target_username

    return JsonResponse({
        "comment": serialized,
        "root_parent_id": root_parent.id,
        "total_comment_count": root_parent.post.comments.count(),
    })


@require_POST
def delete_comment(request, comment_id):
    viewer = _profile(request.user)
    if not viewer:
        return JsonResponse({"error": "auth"}, status=403)
    comment = get_object_or_404(Comment.objects.select_related("post__profile", "author"), id=comment_id)
    is_staff = bool(hasattr(viewer.username, "is_staff") and viewer.username.is_staff)
    if comment.author_id != viewer.id and comment.post.profile_id != viewer.id and not is_staff:
        return JsonResponse({"error": "permission_denied"}, status=403)

    post = comment.post
    comment.delete()
    return JsonResponse({
        "success": True,
        "total_comment_count": post.comments.count(),
    })


def detailed_post(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("profile__username").prefetch_related("likes", "comments"),
        id=post_id,
    )
    viewer = _profile(request.user)

    top_comments = (
        post.comments.filter(parent__isnull=True)
        .select_related("author__username", "post__profile")
        .prefetch_related(
            "likes",
            "replies__author__username",
            "replies__likes",
            "replies__post__profile",
            "replies__parent__author__username",
        )
        .order_by("-created_at")
    )

    comments_data = [_serialize_comment(c, viewer) for c in top_comments]
    is_staff = bool(viewer and hasattr(viewer.username, "is_staff") and viewer.username.is_staff)
    can_delete_post = bool(viewer and (viewer.id == post.profile_id or is_staff))

    context = {
        "post": post,
        "profile": viewer,
        "comments_data": comments_data,
        "post_liked": bool(viewer and post.likes.filter(id=viewer.id).exists()),
        "post_like_count": post.likes.count(),
        "total_comment_count": post.comments.count(),
        "can_delete_post": can_delete_post,
    }
    return render(request, "home/detailed_post.html", context)


# ---------- STORY ENDPOINTS ----------
def create_story(request):
    if not request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.POST.get("ajax"):
            return JsonResponse({"error": "Authentication required"}, status=401)
        return redirect("login")

    profile_obj = _profile(request.user)
    if not profile_obj:
        return JsonResponse({"error": "Profile not found"}, status=404)

    if request.method == "POST":
        # Supports multiple media uploads in one batch
        media_files = request.FILES.getlist("media")
        captions = request.POST.getlist("captions")
        global_caption = request.POST.get("caption", "").strip()

        # Fallback to single image / video if 'media' was not used
        single_image = request.FILES.get("image")
        single_video = request.FILES.get("video")
        if not media_files and (single_image or single_video):
            media_files = [f for f in (single_image, single_video) if f]

        if not media_files:
            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.POST.get("ajax"):
                return JsonResponse({"error": "Please provide at least one photo or video."}, status=400)
            return redirect("home")

        created_stories = []
        for idx, f in enumerate(media_files):
            cap = captions[idx].strip() if idx < len(captions) and captions[idx].strip() else global_caption
            content_type = getattr(f, "content_type", "") or ""
            name_lower = (f.name or "").lower()
            is_video = (
                content_type.startswith("video/")
                or name_lower.endswith((".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v"))
            )

            story = Story.objects.create(
                profile=profile_obj,
                image=None if is_video else f,
                video=f if is_video else None,
                caption=cap,
            )
            created_stories.append(_serialize_story(story, profile_obj))

        if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.POST.get("ajax"):
            return JsonResponse({
                "success": True,
                "count": len(created_stories),
                "stories": created_stories,
                "story": created_stories[0] if created_stories else None,
            })
        return redirect("home")

    return redirect("home")


@require_POST
def toggle_story_like(request, story_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    profile_obj = _profile(request.user)
    if not profile_obj:
        return JsonResponse({"error": "Profile not found"}, status=404)

    story = get_object_or_404(Story, id=story_id)
    if story.likes.filter(id=profile_obj.id).exists():
        story.likes.remove(profile_obj)
        liked = False
    else:
        story.likes.add(profile_obj)
        if story.profile_id != profile_obj.id:
            story.viewers.add(profile_obj)
        liked = True

    return JsonResponse({
        "success": True,
        "story_id": story.id,
        "liked": liked,
        "likes_count": story.likes.count(),
    })


@require_POST
def mark_story_viewed(request, story_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    profile_obj = _profile(request.user)
    if not profile_obj:
        return JsonResponse({"error": "Profile not found"}, status=404)

    story = get_object_or_404(Story, id=story_id)
    if story.profile_id != profile_obj.id:
        story.viewers.add(profile_obj)

    return JsonResponse({
        "success": True,
        "story_id": story.id,
        "viewers_count": story.viewers.count(),
    })


def story_viewers_list(request, story_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    profile_obj = _profile(request.user)
    if not profile_obj:
        return JsonResponse({"error": "Profile not found"}, status=404)

    story = get_object_or_404(
        Story.objects.select_related("profile__username"),
        id=story_id
    )
    is_staff = bool(hasattr(profile_obj.username, "is_staff") and profile_obj.username.is_staff)
    if story.profile_id != profile_obj.id and not is_staff:
        return JsonResponse({"error": "Permission denied"}, status=403)

    viewers_qs = story.viewers.select_related("username").all()
    liked_ids = set(story.likes.values_list("id", flat=True))

    viewers = []
    for v in viewers_qs:
        viewers.append({
            "id": v.id,
            "username": _username(v),
            "name": f"{getattr(v, 'f_name', '')} {getattr(v, 'l_name', '')}".strip() or _username(v),
            "avatar": _avatar(v),
            "liked": v.id in liked_ids,
        })

    viewers.sort(key=lambda x: (not x["liked"], x["name"].lower()))

    return JsonResponse({
        "success": True,
        "story_id": story.id,
        "views_count": len(viewers),
        "likes_count": len(liked_ids),
        "viewers": viewers,
    })


@require_POST
def delete_story(request, story_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    profile_obj = _profile(request.user)
    if not profile_obj:
        return JsonResponse({"error": "Profile not found"}, status=404)

    story = get_object_or_404(Story, id=story_id)
    is_staff = bool(hasattr(profile_obj.username, "is_staff") and profile_obj.username.is_staff)
    if story.profile_id != profile_obj.id and not is_staff:
        return JsonResponse({"error": "Permission denied"}, status=403)

    story.delete()
    return JsonResponse({"success": True, "story_id": story_id})