""" urls for the terms app """
from django.urls import path
from servers import views


urlpatterns = [
    path("", views.index, name='Server index'),
    path("add/", views.add, name='Add server'),
    path("view/<svrid>", views.view, name='Server view'),
    path("svrget/<svrid>", views.svrget, name='Server ontology update (JS)'),
    path("ontupd/<svrid>", views.ontupd, name='Load onts in server to DB'),
    path("updontcnt/<svrid>", views.updontcnt, name='Update term count in DB'),
    path("updontvrs/<svrid>", views.updontvrs, name='Update version in DB'),
]
