from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateListing, CreateBid, CreateComment
from django.contrib.auth.decorators import login_required


from .models import Listing, Comments, Bids, Comments, Category, User


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password")
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
            messages.error(request, "Passwords must match")
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken")
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def create(request):
    form = CreateListing()
    if request.method == "POST":
        form = CreateListing(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.username = request.user
            instance.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": form,
    })

@login_required(login_url='/login')
def listing(request, order_id):

    form = CreateBid()
    listings = Listing.objects.get(pk=order_id)
    comment=Comments.objects.filter(comment_item=order_id)
    bids = Bids.objects.filter(pk=order_id).count()
    user = request.user
    if request.method == "POST":
        form = CreateBid(request.POST)
        if form.is_valid():
            current_price = listings.price
            bid_price = form.cleaned_data['bid']
            instance = form.save(commit=False)
            instance.user = request.user
            instance.bid_item = listings

            if current_price < bid_price:
                Listing.objects.filter(pk=order_id).update(price=bid_price)
                instance.save()
                messages.success(request, 'Bid was successful')
                return HttpResponseRedirect(reverse('listing', args=[order_id]))
            else:
                messages.error(request, 'Bid should be greater than current price')
                return HttpResponseRedirect(reverse('listing', args=[order_id]))
        else:
            return render(request, "auctions/listings.html", {
                "message": "Invalid Form"
            })
    else:
        return render(request, "auctions/listings.html", {
            "listings": listings,
            "form": form,
            "forms": CreateComment(),
            "id": order_id,
            "comment": comment,
            "user": request.user,
            "watched": request.user.watchlist.filter(pk=order_id),
            "bids": bids

        })


def closedlisting(request, sold_id):
    Listing.objects.filter(pk=sold_id).update(active=False)
    list = Listing.objects.get(pk=sold_id)
    winner = Bids.objects.filter(bid_item=list).last().user
    list.winner_user = winner
    list.save()
    return HttpResponseRedirect(reverse('listing', args=[sold_id]))

def comment(request, comment_id):
    form = CreateComment()
    comment = Listing.objects.get(pk=comment_id)

    if request.method == "POST":
        form = CreateComment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.username = request.user
            instance.comment_item = comment
            instance.save()
            messages.success(request, "Comment has been added")
            return HttpResponseRedirect(reverse('listing', args=[comment_id]))

def add_watchlist(request, watchlist_id):
    listing = Listing.objects.get(pk=watchlist_id)
    listing.watched.add(request.user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[watchlist_id]))

def remove_watchlist(request, watchlist_id):
    listing = Listing.objects.get(pk=watchlist_id)
    listing.watched.remove(request.user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[watchlist_id]))

@login_required(login_url='/login')
def watchlist(request):
    watchlists = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlists
    })

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {
        "category": categories
    })

def categories(request, category):
    item = Category.objects.get(name=category)
    categories = item.categories.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
