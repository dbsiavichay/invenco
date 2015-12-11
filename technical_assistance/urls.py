from django.conf.urls import patterns, url
from .views import MaintenanceListView, MaintenanceDetailView

urlpatterns = patterns('',
    url(r'^maintenances/$', MaintenanceListView.as_view(), name='maintenance_list'),
    url(r'^maintenances/(?P<pk>\d+)/$', MaintenanceDetailView.as_view(), name='maintenance_detail'),
)