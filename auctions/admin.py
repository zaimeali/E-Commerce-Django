from django.contrib import admin

from .models import Category, Listing, WatchList, Comment, Bid


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'active', 'listed_by', 'category')


class WatchListAdmin(admin.ModelAdmin):
    list_display = ('id', 'added_item', 'added_by')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_by', 'listing', 'comments')


# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
admin.site.register(Category, CategoryAdmin)
admin.site.register(WatchList, WatchListAdmin)
