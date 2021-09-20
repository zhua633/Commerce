from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm


from .models import Listing, User

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'price', 'description', 'image']

##@login_required
def new_listing(request):
    if request.method == "POST":
        ##user = User.objects.get(username=request.user)
        form = NewListingForm(request.POST)
        if form.is_valid():
            listing=form.save(commit=False)
            ##listing.owner=user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/new_listing.html",{"form":form})

    return render(request,"auctions/new_listing.html",{"form":NewListingForm()})


def index(request):
    return render(request, "auctions/index.html",{"listings":Listing.objects.all()})

def item(request,listing_id):
    iteminfo = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/item.html",{"listing_id":listing_id,"listings":iteminfo})



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
