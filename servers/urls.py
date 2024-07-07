""" urls for the terms app """
from django.urls import path
from servers import views


urlpatterns = [
    path("", views.index, name='Server index'),
    path("add/", views.add, name='Add server'),
    path("view/<svrid>", views.view, name='Server view'),
    path("svrget/<svrid>", views.svrget, name='Server ontology update (JS)'),
    path("svrupd/<svrid>", views.svrupd, name='Load onts in server to DB'),
]
