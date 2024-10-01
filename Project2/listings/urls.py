from django.urls import path
from . import views

urlpatterns = [
    path("<int:listing_id>/", views.listing_detail, name="listing_detail"),
    path("<int:listing_id>/add_bid/", views.add_bid, name="add_bid"),
    path("<int:listing_id>/add_watchlist/",views.add_watchlist,name="add_watchlist"),
    path("<int:listing_id>/delete_watchlist/",views.delete_watchlist,name="delete_watchlist"),
    path("<int:listing_id>/add_comment",views.add_comment,name="add_comment"),
    path("<int:listing_id>/close_auction",views.close_auction,name="close_auction")

]
