from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entries/<str:title>", views.entry, name="entry"),
    path("add", views.add_page, name="add"),
    path("not_found", views.not_found, name="not_found"),
]
