from django.conf.urls import patterns, url
from rest_framework import routers
from .views import ProviderViewSet

purchases_router = routers.DefaultRouter()
purchases_router.register(r'providers', ProviderViewSet)
