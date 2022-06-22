from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search,name="search"),
    path("create", views.createnewpage, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")

]