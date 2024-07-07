""" SciContext Project URL Configuration """
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contexts import views

urlpatterns = [
    path('', views.home, name='SciContext homepage'),
    path('contexts/', include('contexts.urls')),
    path('fields/', include('fields.urls')),
    path('onts/', include('onts.urls')),
    path('projects/', include('projects.urls')),
    path('servers/', include('servers.urls')),
    path('terms/', include('terms.urls')),
]
