from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("user/<int:user_id>", views.user_listing, name="user_listing"),
    path("categories", views.all_categories, name="all_categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("list/create", views.create_listing, name="create_listing"),
    path("list/new", views.new_listing, name="new_listing"),
    path("categories/<int:category_id>",
         views.get_category, name="get_category"),
    path("listing/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("listing/delete_watchlist",
         views.delete_watchlist, name="delete_watchlist"),
    path("list/<int:listing_id>/comment",
         views.add_comment, name="add_comment"),
    path("list/<int:listing_id>/bid", views.create_bid, name="create_bid"),
    path("list/<int:listing_id>/close",
         views.close_listing, name="close_listing"),
    path("list/<int:listing_id>/inactive",
         views.inactive_listing, name="inactive_listing"),
    path("list/<int:listing_id>/active",
         views.active_listing, name="active_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
