from django.contrib.auth import authenticate, login, logout
import json
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *

def index(request, i=1):
    posts = Post.objects.all().order_by('-creation_date')
    paginator = Paginator(posts, 10) #a paginator would have 10 posts only
    postsUI= paginator.page(i)
    #p.num_pages has the numbers of pages possible (we need to send it so we can load the paginator in the front side with bootstrap)
    return render(request, "network/index.html", 
                  {"posts": postsUI,
                   "paginator": paginator
                   })

@login_required
def new_post(request):
    if (request.method == 'POST'):
        new_post = Post(
            content=request.POST['content'],
            owner= request.user
        )
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    


def likes(request, post_id):
    post = Post.objects.get(pk=post_id)
    user_has_liked= False
    if request.user.is_authenticated: 
        user_has_liked = request.user.has_liked(post)
    return JsonResponse({
        "likes_count": post.likes.count(),
        "user_has_liked": user_has_liked
    })


#an api that will return the count of followers and followings, and also if the current user is following the user
def follows_count(request, user_id):
    if request.method == "GET":
        user = User.objects.get(pk=user_id)
        is_following = request.user.is_authenticated and request.user in user.followers.all()
        
        return JsonResponse({
            "followers_count": user.followers.count(),
            "followings_count": user.followings.count(),
            "followed": is_following
        })
        
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
@csrf_exempt
def update_post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
            data = json.loads(request.body)
            new_content = data.get('content')
            
            if post.author != request.user:
                return JsonResponse({"success": False, "error": "You are not authorized to edit this post."}, status=403)

            if new_content:
                post.content = new_content
                post.save()

                return JsonResponse({"success": True, "message": "Post updated successfully."}, status=200)
            else:
                return JsonResponse({"success": False, "error": "Content cannot be empty."}, status=400)

        except Post.DoesNotExist:
            return JsonResponse({"success": False, "error": "Post not found."}, status=404)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


def profile_load(request,user_id,i=1):
    user= User(pk=user_id)
    posts= Post.objects.filter(owner=user).order_by('-creation_date')    
    paginator = Paginator(posts, 10)
    postsUI= paginator.page(i)
    return render(request, "network/profile.html", {
                "posts": postsUI,
                "user":user,
                "paginator": paginator
                })



    
@csrf_exempt
@login_required
def toggle_like(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    try:
        like = Like.objects.get(owner=request.user, post=post)
        like.delete()
    except Like.DoesNotExist:
        Like.objects.create(owner=request.user, post=post)

    return JsonResponse({"message": "Toggle-like-Success"}, status=200)

@csrf_exempt
@login_required
def toggle_follow(request, user_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        action = data.get("action")
        
        try:
            user_to_follow = User.objects.get(pk=user_id)
            if action == "follow":
                request.user.followings.add(user_to_follow)
                message = "Followed successfully"
            elif action == "unfollow":
                request.user.followings.remove(user_to_follow)
                message = "Unfollowed successfully"
            else:
                return JsonResponse({"error": "Invalid action"}, status=400)
            
            return JsonResponse({"message": message}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def following(request,i=1):
    posts = Post.objects.filter(owner__in=request.user.followings.all()).order_by('-creation_date')
    #__in is used to filter posts where the owner is one of these users.
    paginator = Paginator(posts, 10) #a paginator would have 10 posts only
    postsUI= paginator.page(i)
    #p.num_pages has the numbers of pages possible (we need to send it so we can load the paginator in the front side with bootstrap)
    return render(request, "network/following.html", 
                  {"posts": postsUI,
                   "paginator": paginator
                   })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
