from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import User, Listing, Watchlist,Category, Comment


def index(request):
    listings = Listing.objects.all().filter(is_active=True)
    watchlist_count = 0
    header_title="Active listings"
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        if watchlist:
            watchlist_count = watchlist.listings.count()
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "header_title":header_title,
        "categories": Category.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



@login_required
def watchlist_listings(request):
    watchlist_count = 0
    listings = []
    header_title= "Listings in your watchlist"
    watchlist = Watchlist.objects.filter(user=request.user).first()
    if watchlist:
        watchlist_count = watchlist.listings.count()
        listings = watchlist.listings.all()
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "header_title":header_title,
        "categories": Category.objects.all()
    })
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def category(request,id):
    category_x= Category.objects.get(pk=id) 
    listings= category_x.listings.all()
    watchlist_count = 0
    header_title=f"listings: {category_x.name}"
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        if watchlist:
            watchlist_count = watchlist.listings.count()
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "header_title":header_title,
        "categories": Category.objects.all()
    })
    
    
@login_required
def create_listing(request):
    watchlist_count=0
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category_id = request.POST["category"]
        image = request.POST["image_url"]
        owner= request.user

        category = Category.objects.get(id=category_id)

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            category=category,
            image_url=image,
            owner=owner
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    elif request.method == "GET":
        watchlist = Watchlist.objects.filter(user=request.user).first()
        if watchlist:
            watchlist_count = watchlist.listings.count()

        return render(request, "auctions/create_listing.html", {
            "watchlist_count": watchlist_count,
            "categories": Category.objects.all()
        })


@login_required
def user_listings(request):
    watchlist_count = 0
    listings = []
    header_title= "Your listings"
    watchlist = Watchlist.objects.filter(user=request.user).first()
    if watchlist:
        watchlist_count = watchlist.listings.count()

    listings= Listing.objects.all().filter(owner=request.user)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "header_title":header_title,
        "categories": Category.objects.all()
    })
    

@login_required
def won_listings(request):
    watchlist_count = 0
    listings = []
    header_title= "Listings you won"
    watchlist = Watchlist.objects.filter(user=request.user).first()
    if watchlist:
        watchlist_count = watchlist.listings.count()

    listings= Listing.objects.all().filter(winner=request.user)
    print(listings)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "header_title":header_title,
        "categories": Category.objects.all()
    })
    