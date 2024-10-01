from django.shortcuts import render,HttpResponseRedirect, redirect
from auctions.models import Listing, User, Bid, Watchlist,Category, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

def listing_detail(request, listing_id):
    watchlist_count=0
    is_in_watchlist = False
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        if watchlist:
            is_in_watchlist = watchlist.listings.filter(pk=listing_id).exists()
            watchlist_count = watchlist.listings.count()
        
    listing = Listing.objects.filter(pk=listing_id).first()
    
    if listing:
        bid_count= listing.bid.count() 
        return render(request, 'auctions/listing.html', {
                                                        'listing': listing,
                                                        'watchlist_count':watchlist_count,
                                                        'bid_count': bid_count,
                                                        'is_in_watchlist': is_in_watchlist,
                                                        'categories': Category.objects.all()
                                                         })
    else:
        return render(request, 'auctions/404.html', status=404)

@login_required
def add_watchlist(request, listing_id):
    user= request.user
    listing = Listing.objects.get(pk=listing_id)

    #if this user has a watchlist
    if hasattr(user, 'watchlist'):
        watchlist = user.watchlist
    else:
        watchlist = Watchlist.objects.create(user=user)

    watchlist.listings.add(listing)

    return HttpResponseRedirect(reverse("listing_detail",kwargs={'listing_id':listing_id}))


@login_required
def delete_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    
    try:
        watchlist = Watchlist.objects.get(user=user)
    except Watchlist.DoesNotExist:
        watchlist = None
    
    if watchlist and listing in watchlist.listings.all():
        watchlist.listings.remove(listing)
        
    return HttpResponseRedirect(reverse("listing_detail", kwargs={'listing_id': listing_id}))




@login_required
def add_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.filter(user=request.user).first()
    watchlist_count=0
    if watchlist:
        watchlist_count = watchlist.listings.count()
        
    try:
        bid_value = float(request.POST.get("bid"))
    except (ValueError, TypeError):
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'error_message': "Your bid must be a valid number.",
            'watchlist_count':watchlist_count
        })

    if listing.bid.exists():
        current_bid = listing.bid.last().bid_value
        if bid_value > current_bid:
            bid = Bid(listing=listing, user=request.user, bid_value=bid_value)
            bid.save()
            return HttpResponseRedirect(reverse("listing_detail", kwargs={'listing_id': listing_id}))
        else:
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'error_message': f"Your bid must be higher than the current bid of ${current_bid}.",
                'watchlist_count':watchlist_count
            })
    else:
        if bid_value >= listing.starting_bid:
            bid = Bid(listing=listing, user=request.user, bid_value=bid_value)
            bid.save()
            return HttpResponseRedirect(reverse("listing_detail", kwargs={'listing_id': listing_id}))

        else:
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'error_message': f"Your bid must be at least the starting bid of ${listing.starting_bid}.",
                'watchlist_count':watchlist_count
            })
      
    
@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.filter(pk=listing_id).first()
        content = request.POST["content"]

        comment = Comment(
            user=request.user,
            listing=listing,
            content=content
        )
        comment.save()
        
        return HttpResponseRedirect(reverse('listing_detail', kwargs={'listing_id':listing_id }))
            

            
@login_required
def close_auction(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    if listing.bid.exists():
        listing.winner= listing.bid.last().user
    else:
        listing.winner= None
    listing.save()
    return HttpResponseRedirect(reverse('listing_detail', kwargs={'listing_id':listing_id }))
