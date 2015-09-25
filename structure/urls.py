from django.conf.urls import patterns, url
from .views	import JobListView, JobDetailView

urlpatterns = patterns('',
    url(r'^jobs/$', JobListView.as_view(), name='job_list'),
    url(r'^jobs/(?P<pk>\d+)/$', JobDetailView.as_view(), name='job_detail'),
)