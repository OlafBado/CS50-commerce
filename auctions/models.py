from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime, date


class User(AbstractUser):
    pass

class Auction(models.Model):
    #ALL = 'All'
    #HOME = 'Home'
    #FASHION = 'Fashion'
    #TOYS = 'Toys'
    #ELECTRONICS = 'Electronics'
    #COMMODITY = 'Commodity'
    category_choices = [
        ('All', 'All'),
        ('Home', 'Home'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Commodity', 'Commodity')
    ]
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50, blank=True)
    bid = models.DecimalField(decimal_places=2, max_digits=19)
    category = models.CharField(max_length=30, choices=category_choices, blank=True)
    url = models.URLField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    #additional field for users watchlist
    users_watchlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_watchlist", blank=True)
    #field for user that created listing
    #user = models.CharField(max_length=30, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bids(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bidding', default=1)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bidding', default=1)
    new_bid = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.auction} | {self.new_bid}"

class Comments(models.Model):

    #which comments are connected to which auction?
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments", default=1)
    name = models.CharField(max_length=30, default=1)
    email = models.EmailField(default=1)
    content = models.TextField(default=1)
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        #order by date
        ordering = ("publish",)
    
    def __str__(self):
        return f"Comment by {self.name}"