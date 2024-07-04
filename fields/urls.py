""" urls for the fields app """
from django.urls import path
from fields import views


urlpatterns = [
    path("index/", views.index, name='Field index'),
    path("view/<fldid>", views.view, name='Field view'),
]
