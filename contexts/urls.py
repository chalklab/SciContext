""" urls for the contexts app """
from django.urls import path
from contexts import views


urlpatterns = [
    path("", views.index, name='Context index'),
    path("add/", views.add, name='Context add'),
    path("view/<ctxid>", views.view, name='Context view'),
    path("write/<ctxid>", views.jswrtctx, name='Context write'),
]
