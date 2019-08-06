from django.conf.urls import include, url
from rest_framework import routers

urlpatterns = [
    url('^', include('api.urls')),
               #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

