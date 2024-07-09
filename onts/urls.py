""" urls for the onts app """
from django.urls import path
from onts import views


urlpatterns = [
    path("", views.index, name='Ontology index'),
    path("view/<ontid>", views.view, name='Ontology view'),
    path("ontget/<svrid>", views.ontget, name='Server ontology update (JS)'),
    path("ontupd/<svrid>", views.ontupd, name='Load onts in server to DB'),
    path("bysvr/<svrid>", views.bysvr, name='Ontology list by server'),
]
