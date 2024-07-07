""" urls for the projects app """
from django.urls import path
from projects import views


urlpatterns = [
    path("", views.index, name='Project index'),
    path("add/", views.add, name='Add project'),
    path("view/<prjid>", views.view, name='Project view'),
]
