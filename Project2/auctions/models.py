from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=24, decimal_places=2)
    image_url = models.URLField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="won_listing", blank=True)
    creation_date = models.DateTimeField(auto_now_add=True,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_listings",null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title


class Bid(models.Model):
    bid_value = models.DecimalField(max_digits=24, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids",null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid",null=True)
    def __str__(self):
        return f'{self.bid_value} - {self.user} on {self.listing}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.user} on {self.listing}'


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    def __str__(self):
        return f'{self.user}\'s Watchlist'
