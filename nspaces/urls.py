""" urls for the nspaces app """
from django.urls import path
from nspaces import views


urlpatterns = [
    path("index/", views.index, name='Namespace index'),
    path("view/<nspid>", views.view, name='Namespace view'),
]
