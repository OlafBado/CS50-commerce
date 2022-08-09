from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import datetime

from .forms import NewCommentForm
from .models import User, Auction, Bids, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
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

def create_listing(request):

    if request.method == "POST":
        title = request.POST["title"]
        bid = request.POST["bid"]
        description = request.POST["description"]
        url = request.POST["url"]
        category = request.POST["category"]
        author = request.user
        listing = Auction(author=author, title=title, bid=bid, description=description, url=url, category=category)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html")



def listings(request, auction_id):
    
    count = Bids.objects.filter(auction=auction_id)
    count_global = len(count)
    user_comment = None
    #comments for individual auction
    comments = Comments.objects.filter(auction=auction_id)

    if request.method == "POST":

        if "watchlist" in request.POST:
            auction = Auction.objects.get(pk=auction_id)
            if auction.users_watchlist.filter(id=request.user.id).exists():
                auction.users_watchlist.remove(request.user)
            else:
                auction.users_watchlist.add(request.user)
            
        if "bid" in request.POST:
            new_bid = int(request.POST["bid"])
            auction = Auction.objects.get(pk=auction_id)
            if new_bid > auction.bid:
                bid = Bids(user=request.user, auction=auction, new_bid=new_bid, bid_time=datetime.datetime.now())
                bid.save()
                auction.bid = new_bid
                auction.save()
                return HttpResponseRedirect(reverse("listings", args=(auction_id,)))
            else:
                return render(request, "auctions/listings.html", {
                    "message": "Bid must be greater than current bid!",
                    "auction": Auction.objects.get(pk=auction_id),
                    "count": count_global,
                    "comment_form": NewCommentForm(),
                    "comments": comments,
                })

        if "delete" in request.POST:
            auction = Auction.objects.get(id=auction_id)
            if request.user == auction.author:
                #zwraca wiersze dla danej aukcji, sortuje wedlug najwiekszego bida i zwraca najwiekszy bid
                bids = Bids.objects.filter(auction=auction_id).order_by('-new_bid').first()
                #sprawdza czy ktos wgl bidowal, jesli nie to usuwa
                if bids == None:
                    auction.delete()
                    return HttpResponseRedirect(reverse("index"))
                else:
                    #zmienna która trzyma uzytkownika najwiekszego bida
                    auction.delete()
                    winner = bids.user
                    winner_bid = bids.new_bid         
                    return render(request, "auctions/close.html", {
                            "winner": winner,
                            "bid": winner_bid
                        })
            else:
                return render(request, "auctions/listings.html", {
                    "message1": "You can't close somebody's auction!",
                    "auction": Auction.objects.get(pk=auction_id),
                    "count": count_global,
                    "comment_form": NewCommentForm(),
                    "comments": comments,
                })

        if "comment" in request.POST:
            #collect all information
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                name = request.POST["name"]
                email = request.POST["email"]
                content = request.POST["content"]
                auction = Auction.objects.get(id=auction_id)
                comment = Comments(name=name, email=email, content=content, auction=auction)
                comment.save()
                return HttpResponseRedirect(reverse("listings", args=(auction_id,)))


    return render(request, "auctions/listings.html", {
        "auction": Auction.objects.get(pk=auction_id),
        "count": count_global,
        "comment_form": NewCommentForm(),
        "comments": comments,
    })

def watchlist(request):
    auction = Auction.objects.filter(users_watchlist=request.user)    
    return render(request, "auctions/watchlist.html", {
        "auctions": auction
    })

def close(request):
    return render(request, "auctions/close.html")

def categories(request):
    return render(request, "auctions/categories.html", {
        "auctions": Auction.objects.all()
    })

def categories_category(request, category):
    #query for auctions for specific category
    auction = Auction.objects.filter(category=category)
    return render(request, "auctions/categories_category.html", {
        "category": category,
        "auctions": auction
    })