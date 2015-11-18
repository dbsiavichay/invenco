from django.conf.urls import patterns, url
from .views import MaintenanceListView

urlpatterns = patterns('',
    url(r'^maintenances/$', MaintenanceListView.as_view(), name='maintenance_list'),
)