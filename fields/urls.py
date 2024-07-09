""" urls for the fields app """
from django.urls import path
from fields import views


urlpatterns = [
    path("", views.index, name='Field index'),
    path("add/", views.add, name='Add field'),
    path("view/<fldid>", views.view, name='Field view'),
    path("read/<fldid>", views.read, name='Read field data'),
]
