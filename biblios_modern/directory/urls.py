from django.urls import path

from . import views

app_name = "directory"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("biblioteki/", views.LibraryListView.as_view(), name="index"),
    path("biblioteki/<slug:slug>/", views.LibraryDetailView.as_view(), name="detail"),
]
