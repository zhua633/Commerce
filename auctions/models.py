from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField

CLT = "Fashion"
ELEC = "Electronics"
FUR = "Furniture"
TOY = "Toys"
NOV = "Novelty"
STA = "Stationary"
GAR = "Gardening"


CATEGORIES = (
    (CLT, "Fashion"),
    (ELEC, "Electronics"),
    (FUR, "Furniture"),
    (TOY, "Toys"),
    (NOV,"Novelty"),
    (STA,"Stationary"),
    (GAR,"Gardening")

)

class User(AbstractUser):
    pass

class Listing(models.Model):
    listing_id = models.BigAutoField(primary_key=True)
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=255, blank=True)
    starting_bid=models.FloatField(max_length=10)
    time=models.DateTimeField(auto_now_add=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="owner")
    image = models.ImageField(null=True, blank=True)
    offer=models.FloatField(max_length=10,null=True, blank=True)
    category=models.CharField(max_length=20,choices=CATEGORIES,default="Fashion")
    watcher=models.ManyToManyField(User, related_name="watcher_list")
    watched=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.listing_id}.{self.title} has description of : {self.description} is bidded at {self.offer}"


class Bid(models.Model):
    bid_id = models.BigAutoField(primary_key=True)
    user=ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="bidder")
    time=models.DateTimeField(auto_now_add=True, blank=True)
    bid=models.FloatField(max_length=10,null=True, blank=True)

    #Turns objects into a string
    def __str__(self):
        return f"{self.bid_id}: A user bidded {self.bid} at {self.time}"

class Comment(models.Model):
    commenter=ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="commenter")
    comment_id = models.BigAutoField(primary_key=True)
    time=models.DateTimeField(auto_now_add=True, blank=True)
    comments=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.commenter} commented {self.comments} at {self.time}"


class WatchList(models.Model):
    watcher=ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="watcher")
    time=models.DateTimeField(auto_now_add=True, blank=True)
    listing=ManyToManyField(Listing, blank=True, related_name="listing")
    def __str__(self):
        return f"{self.watcher} is watching {self.listing}"

