from django.conf.urls import url
from .views import *

urlpatterns = [	
    url(r'^building/$', BuildingListView.as_view(), name='building_list'),
    url(r'^building/add/$', BuildingCreateView.as_view(), name='building_create'),
    url(r'^building/(?P<pk>\d+)/edit/$', BuildingUpdateView.as_view(), name='building_update'),
    url(r'^building/(?P<pk>\d+)/delete/$', BuildingDeleteView.as_view(), name='building_delete'),
]