""" urls for the terms app """
from django.urls import path
from terms import views


urlpatterns = [
    path("", views.index, name='Term index'),
    path("add/", views.add, name='Add term'),
    path("view/<trmid>", views.view, name='Term view'),
]
