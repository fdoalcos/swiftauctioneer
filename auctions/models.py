from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    pass


class pictures(models.Model):
    pass

class Category(models.Model):
    CATEGORIES = ("Groceries & Stores", "Groceries & Stores"), ("Fashion & Beauty", "Fashion & Beauty"), ("Pets", "Pets"), ("Drugstore & Personal Care", "Drugstore & Personal Care"), ("Home & DIY", "Home & DIY"), ("Devices & Electronics", "Devices & Electronics"), ("Music, Video & Gaming", "Music, Video & Gaming"), ("Books & Reading", "Books & Reading"), ("Toys, Kids & Baby", "Toys, Kids & Baby"), ("Automotive", "Automotive"), ("Office & Professional", "Office & Professional"), ("Sports & Fanshop", "Sports & Fanshop"), ("Outdoors & Travels", "Outdoors & Travels"), ("Other", "Other")

    name = models.CharField(max_length=100, choices=CATEGORIES, primary_key=True)
    category_image = models.ImageField(upload_to='category/', blank=True, null=True)


    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):

    username = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user")
    item = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    active = models.BooleanField(default=True)
    price = models.FloatField()
    watched = models.ManyToManyField(User, null=True, related_name="watchlist")
    winner_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,  related_name="winner")

    def __str__(self):
        return f"{self.item} ({self.id})"

    def number_bids(self):
        return self.bid_item.all().count()

    def winner(self):
        return self.bid_item.last().user


class Bids(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bid_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")
    bid = models.FloatField()

    def __str__(self):
        return f"({ self.user }) ~ {self.bid_item}"

class Comments(models.Model):
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_item")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"



