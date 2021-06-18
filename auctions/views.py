from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Category, WatchList, Comment


def index(request):
    listings = Listing.objects.exclude(
        active=False).all().order_by('-created_at')
    # listings = Listing.objects.all().order_by('-created_at')

    numWatchList = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        numWatchList = WatchList.objects.filter(added_by=int(user_id)).count()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "numWatchList": numWatchList
    })


def listing(request, listing_id):
    listing = Listing.objects.get(id=int(listing_id))
    numBids = Bid.objects.filter(bid_on=int(listing_id)).count()

    comments = Comment.objects.filter(listing=int(listing_id))

    bids = Bid.objects.filter(bid_on=int(listing_id)).order_by('-bid')
    # maxBid = Bid.objects.filter(bid_on=int(listing_id)).aggregate(Max('bid'))

    maxBid = 0
    if bids:
        maxBid = bids[0].bid
    else:
        maxBid = listing.price

    numWatchList = 0
    watchlist = None
    if request.user.is_authenticated:
        user_id = request.user.id
        watchlist = WatchList.objects.filter(
            added_item=int(listing_id), added_by=int(user_id)).first()
        numWatchList = WatchList.objects.filter(added_by=int(user_id)).count()

    error = ""

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "numBids": numBids,
        "watchlist": watchlist,
        "numWatchList": numWatchList,
        "comments": comments,
        "bids": bids,
        "maxBid": maxBid,
        "error": error
    })


def user_listing(request, user_id):
    user = User.objects.get(id=int(user_id))
    listings = user.posted_by.all().order_by('-created_at')

    numWatchList = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        numWatchList = WatchList.objects.filter(added_by=int(user_id)).count()

    return render(request, "auctions/user.html", {
        "listings": listings,
        "user": user,
        "numWatchList": numWatchList
    })


def all_categories(request):
    categories = Category.objects.all()

    numWatchList = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        numWatchList = WatchList.objects.filter(added_by=int(user_id)).count()

    return render(request, "auctions/categories.html", {
        "categories": categories,
        "numWatchList": numWatchList
    })


def get_category(request, category_id):
    category = Category.objects.get(id=int(category_id))
    listings = category.category.all().order_by('-created_at')

    numWatchList = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        numWatchList = WatchList.objects.filter(added_by=int(user_id)).count()

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings,
        "numWatchList": numWatchList
    })


def add_watchlist(request):
    if request.user.is_authenticated and request.method == 'POST':
        added_item = int(request.POST['added_item'])
        listing = Listing.objects.get(pk=added_item)
        added_by = int(request.POST['added_by'])
        user = User.objects.get(pk=added_by)
        watchlist = WatchList(added_by=user, added_item=listing)
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(added_item,)))


def delete_watchlist(request):
    if request.user.is_authenticated and request.method == 'POST':
        added_item = int(request.POST['added_item'])
        added_by = int(request.POST['added_by'])
        watchlist = WatchList.objects.filter(
            added_item=added_item, added_by=added_by).delete()
        return HttpResponseRedirect(reverse("listing", args=(added_item,)))


def watchlist(request):
    user_id = request.user.id

    numWatchList = 0
    listing_items = []
    if request.user.is_authenticated:
        numWatchList = WatchList.objects.filter(added_by=int(user_id)).count()
        listings = WatchList.objects.filter(added_by=int(user_id))
        listitem_ids = listings.values_list('added_item', flat=True)
        listing_items = Listing.objects.filter(id__in=listitem_ids)

    return render(request, "auctions/watchlist.html", {
        "numWatchList": numWatchList,
        "listing_items": listing_items
    })


@login_required(login_url="/login")
def create_listing(request):
    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
        "categories": categories
    })


@login_required(login_url="/login")
def new_listing(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            category = Category.objects.get(pk=request.POST['category'])
            listed_by = User.objects.get(pk=user.id)
            status = ''
            if request.POST.get('active') is None:
                status = 'inactive'
            else:
                status = request.POST['active']

            listing = Listing(
                title=request.POST['title'],
                description=request.POST['description'],
                price=request.POST['price'],
                image_url=request.POST['image_url'],
                # active=True if request.POST['active'] == 'active' else False,
                active=True if status == 'active' else False,
                category=category,
                listed_by=listed_by
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def add_comment(request, listing_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=int(user_id))
        listing = Listing.objects.get(pk=int(listing_id))

        comment = Comment(
            comments=request.POST['comment'],
            comment_by=user,
            listing=listing
        )
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="/login")
def create_bid(request, listing_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=int(user_id))
        listing = Listing.objects.get(pk=int(listing_id))
        bid_number = request.POST['bid']

        bids = Bid.objects.filter(bid_on=int(listing_id)).order_by('-bid')

        maxBid = 0
        if bids:
            maxBid = bids[0].bid
        else:
            maxBid = listing.price

        if int(maxBid) > int(bid_number):
            error = 'value_less'
            numBids = Bid.objects.filter(bid_on=int(listing_id)).count()

            comments = Comment.objects.filter(listing=int(listing_id))

            numWatchList = 0
            watchlist = None

            if request.user.is_authenticated:
                user_id = request.user.id
                watchlist = WatchList.objects.filter(
                    added_item=int(listing_id), added_by=int(user_id)).first()
                numWatchList = WatchList.objects.filter(
                    added_by=int(user_id)).count()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "numBids": numBids,
                "watchlist": watchlist,
                "numWatchList": numWatchList,
                "comments": comments,
                "bids": bids,
                "maxBid": maxBid,
                "error": error
            })

        else:
            bid = Bid(
                bid=bid_number,
                bid_on=listing,
                bid_by=user
            )
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="/login")
def inactive_listing(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="/login")
def active_listing(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))
    listing.active = True
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="/login")
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))
    bid = Bid.objects.filter(bid_on=int(listing_id))
    bidCount = bid.count()

    if bidCount > 0:
        maxBid = bid.order_by('-bid')[0]
        user = User.objects.get(pk=int(maxBid.bid_by.id))
        listing.winned_by = user
        listing.active = False
        listing.save()

        # watchlist = WatchList.objects.filter(
        #     added_item=listing, added_by=user).delete()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("inactive_listing", args=(listing_id,)))


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
