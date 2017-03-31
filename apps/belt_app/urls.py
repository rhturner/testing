from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_registration$', views.process_registration),
    url(r'^create$', views.create),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
]
