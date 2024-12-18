from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random", views.random_f, name="random"),
    path("add", views.add_page, name="add"),
    path("<str:not_found>", views.not_found, name="not_found"),
    path("edit/<str:heading>", views.edit, name="edit" )
]
