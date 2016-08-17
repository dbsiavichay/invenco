from django.conf.urls import patterns, url
from rest_framework import routers
from .views	import *

urlpatterns = patterns('',
    url(r'^allocations/$', AllocationListView.as_view(), name='allocation_list'),
    url(r'^allocations/(?P<pk>\d+)/$', AllocationDetailView.as_view(), name='allocation_detail'),
)

allocation_router = routers.DefaultRouter()
allocation_router.register(r'allocations', AllocationViewSet)
