from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("watchlist", views.watchlist_listings, name="watchlist_listings"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listings/', include('listings.urls')),
    path("category/<int:id>", views.category, name="category"),
    path("create_listing",views.create_listing,name="create_listing"),
    path("user_listings",views.user_listings,name="user_listings"),
    path("won_listings",views.won_listings,name="won_listings")
]
