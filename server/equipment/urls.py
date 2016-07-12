from django.conf.urls import patterns, url
from .views	import TrademarkListView, TrademarkDetailView, TypeListView, TypeDetailView, ModelListView, ModelDetailView, DeviceListView, DeviceDetailView, ReportListView
from rest_framework import routers
from .views import *

urlpatterns = patterns('',
    url(r'^trademarks/$', TrademarkListView.as_view(), name='trademark_list'),
    url(r'^trademarks/(?P<pk>\d+)/$', TrademarkDetailView.as_view(), name='trademark_detail'),
    url(r'^types/$', TypeListView.as_view(), name='type_list'),
    url(r'^types/(?P<pk>\d+)/$', TypeDetailView.as_view(), name='type_detail'),
    url(r'^models/$', ModelListView.as_view(), name='model_list'),
    url(r'^models/(?P<pk>\d+)/$', ModelDetailView.as_view(), name='model_detail'),
    url(r'^devices/$', DeviceListView.as_view(), name='device_list'),
    url(r'^devices/(?P<pk>\d+)/$', DeviceDetailView.as_view(), name='device_detail'),
    url(r'^reports/$', ReportListView.as_view(), name='report_list'),
)

equipment_router = routers.DefaultRouter()
equipment_router.register(r'trademarks', TrademarkViewSet)
equipment_router.register(r'types/list', TypeListViewSet)
equipment_router.register(r'types', TypeViewSet)
equipment_router.register(r'models/list', ModelListViewSet)
equipment_router.register(r'models', ModelViewSet)
equipment_router.register(r'devices/list', DeviceListViewSet)
equipment_router.register(r'devices', DeviceViewSet)
