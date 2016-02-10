from django.conf.urls import patterns, url
from .views	import AllocationListView, AllocationDetailView, report_view

urlpatterns = patterns('',
    url(r'^allocations/$', AllocationListView.as_view(), name='allocation_list'),
    url(r'^allocations/(?P<pk>\d+)/$', AllocationDetailView.as_view(), name='allocation_detail'),
    url(r'^reports/$', report_view),
)
