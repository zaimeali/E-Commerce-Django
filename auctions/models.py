from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200, blank=True)
    price = models.IntegerField(default=0)
    image_url = models.TextField(max_length=256)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category", blank=True, null=True)
    listed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posted_by")
    winned_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="won_by")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{ self.title }"


class WatchList(models.Model):
    added_item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="items")
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.added_item} - {self.added_by}"


class Bid(models.Model):
    bid = models.IntegerField()
    bid_on = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_on")
    bid_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_by")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bid} bid is on {self.bid_on} by {self.bid_by}"


class Comment(models.Model):
    comments = models.TextField(max_length=200)
    comment_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commentor")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="item_comment")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment_by} on {self.listing}"
