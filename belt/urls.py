
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.belt_app.urls')),
]
