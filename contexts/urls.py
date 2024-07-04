""" urls for the substances app """
from django.urls import path
from contexts import views


urlpatterns = [
    path("", views.home, name='SciContext home'),
    path("index/", views.index, name='Context index'),
    path("add/", views.add, name='Context add'),
    path("view/<ctxid>", views.view, name='Context view'),
    path("write/<ctxid>", views.jswrtctx, name='Context write'),
]
