from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path('', views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:edit>", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("<str:search>", views.search, name="search"),
    path("find/", views.find, name="find")
]