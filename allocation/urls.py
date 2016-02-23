from django.conf.urls import patterns, url
from .views	import AllocationListView, AllocationDetailView

urlpatterns = patterns('',
    url(r'^allocations/$', AllocationListView.as_view(), name='allocation_list'),
    url(r'^allocations/(?P<pk>\d+)/$', AllocationDetailView.as_view(), name='allocation_detail'),
)
