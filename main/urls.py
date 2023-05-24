from django.urls import path

from . import views

app_name = "main" 
urlpatterns = [
    path("search/", views.search, name="search"),
    path("select_category/", views.select_category, name="select_category"),
    path("", views.index, name="index"),
]
