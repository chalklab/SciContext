""" urls for the terms app """
from django.urls import path
from terms import views


urlpatterns = [
    path("index/", views.index, name='Term index'),
    path("view/<trmid>", views.view, name='Term view'),
]
