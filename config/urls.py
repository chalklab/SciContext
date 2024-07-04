""" SciContext Project URL Configuration """
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contexts import views

urlpatterns = [
    path('', views.home, name='SciContext homepage'),
    path('contexts/', include('contexts.urls')),
    path('fields/', include('fields.urls')),
    path('nspaces/', include('nspaces.urls')),
    path('terms/', include('terms.urls')),
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
