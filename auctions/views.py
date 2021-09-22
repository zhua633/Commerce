from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm
from .models import User,Listing,WatchList,Comment,Bid, CATEGORIES
from django.utils.safestring import mark_safe

'''
class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value is not None:
            img_html = mark_safe(f'<br><br><img src="{value.url}"/>')
            return f'{input_html}{img_html}'
        else:
            return None

'''


class NewListingForm(ModelForm):
    ##images = forms.ImageField(widget=ImagePreviewWidget, required=False)
    class Meta:
        model = Listing
        fields = ['title', 'category','starting_bid', 'description','image']



class NewCommentForm(ModelForm):
    class Meta:
        model= Comment
        fields=['comments']

class NewBidForm(ModelForm):
    class Meta:
        model= Bid
        fields=['bid']

@login_required(login_url="login")
def new_listing(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = NewListingForm(request.POST,request.FILES)
        if form.is_valid():
            listing=form.save(commit=False)
            listing.owner=user
            listing.save()
            return render(request,"auctions/index.html",{"listings":Listing.objects.all()})
        else:
            return render(request,"auctions/new_listing.html",{"form":form})

    return render(request,"auctions/new_listing.html",{"form":NewListingForm()})


def index(request):
    return render(request, "auctions/index.html",{"listings":Listing.objects.all()})

def final(request,listing_id):
    Listing.closed=True
    iteminfo = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/final.html",{"offer":iteminfo.offer,"buyer":iteminfo.buyer})

def item(request,listing_id):
    iteminfo = Listing.objects.get(pk=listing_id)
    Comments=Comment.objects.all()
    bid_form=None
    comment_form=None

    if request.method == "POST":
        # Check if loggedin
        bid_form=NewBidForm(request.POST)
        comment_form=NewCommentForm(request.POST)
        try:
            user = User.objects.get(username=request.user)

            if bid_form.is_valid():
                Bids=bid_form.save(commit=False)
                Bids.bidder=user
                iteminfo.buyer=user
                Bids.save()
                if (Bids.bid>iteminfo.offer):
                    iteminfo.offer=Bids.bid
                    iteminfo.save()

            if comment_form.is_valid():
                Comments=comment_form.save(commit=False)
                Comments.commenter=user
                Comments.save()

        except  User.DoesNotExist:
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/item.html", {
            "listing_id":listing_id,
            "listings":iteminfo,
            "Comments":Comment.objects.all(),
            "bid_form":NewBidForm(),
            "comment_form":NewCommentForm()
        })
    return render(request, "auctions/item.html", {
    "listing_id":listing_id,
    "listings":iteminfo,
    "Comments":Comment.objects.all(),
    "bid_form":NewBidForm(),
    "comment_form":NewCommentForm()
})

@login_required(login_url="login")
def watchlist(request,listing_id):
    iteminfo = Listing.objects.get(pk=listing_id)
    listing=iteminfo.listing.all()

    try:
        watchlist = WatchList.objects.get(watcher=request.user)
    except WatchList.DoesNotExist:
        watchlist = None

    if iteminfo in watchlist.listing.all():
        if (watchlist is not None):
            watchlist.listing.remove(iteminfo)
            watchlist.save()
            iteminfo.watched=False
            iteminfo.save()
            listing=watchlist.listing.all()
        else:
            listing=None
        return render(request, "auctions/watchlist.html",{"listings":listing})
    else:
        watchlist.listing.add(iteminfo)
        watchlist.save()
        iteminfo.watched=True
        iteminfo.save()
        listing=watchlist.listing.all()
        return render(request, "auctions/watchlist.html",{"listings":listing})



def categories(request):
    cat=[]
    for rows in CATEGORIES:
        cat.append(rows[0])
    return render(request, "auctions/categories.html", {
        "categories" : cat
    })

def category(request,name):
    list_id=[]
    cat = Listing.objects.all()
    for x in cat:
        if x.category==name:
            list_id.append(x.listing_id)

    return render(request, "auctions/category.html", {
        "categories" : list_id
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
            WatchList.objects.create(watcher=user)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

