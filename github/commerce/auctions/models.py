from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Listing(models.Model):
    listing_id = models.BigAutoField(primary_key=True)
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=255, blank=True)
    price=models.FloatField(max_length=10)
    time=models.DateTimeField(null=True)
    ##owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.listing_id}.{self.title} has description of : {self.description} is selling at {self.price}"

'''
class Bid(models.Model):
    bid_id=models.IntegerField()
    user=ForeignKey(User, on_delete=models.CASCADE, realted_name="user")
    time=models.DateTimeField()
    bid=models.FloatField()
    offer=models.FloatField()

    #Turns objects into a string
    def __str__(self):
        return f"{self.bid_id}: {self.user} bidded {self.bid} at {self.time}"

    
    
class Comment(models.Model):
    user=ForeignKey(User, on_delete=models.CASCADE, realted_name="user")
    time=models.DateTimeField()
    comments=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user} commented {self.comments} at {self.time}"


class Listing(models.Model):
    item=models.CharField(max_letngth=64)
    description=models.CharField(max_length=255)
    price=models.FloatField()
    time=models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.item} has description of : {self.description} is selling at {self.price}"
'''