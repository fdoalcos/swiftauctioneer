from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:order_id>", views.listing, name="listing"),
    path("closelisting/<int:sold_id>", views.closedlisting, name="close"),
    path("<int:comment_id>", views.comment, name="comment"),
    path("watchlist/<int:watchlist_id>", views.add_watchlist, name="watch"),
    path("remove_watchlist/<int:watchlist_id>", views.remove_watchlist, name="remove"),
    path("watchlist", views.watchlist, name="watches"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.categories, name="categories")
]