from django.conf.urls import patterns, url
from .views	import JobListView, JobDetailView, DepartmentListView, DepartmentDetailView, AreaListView, AreaDetailView

urlpatterns = patterns('',
    url(r'^jobs/$', JobListView.as_view(), name='job_list'),
    url(r'^jobs/(?P<pk>\d+)/$', JobDetailView.as_view(), name='job_detail'),
    url(r'^departments/$', DepartmentListView.as_view(), name='department_list'),
    url(r'^departments/(?P<pk>\d+)/$', DepartmentDetailView.as_view(), name='department_detail'),
    url(r'^areas/$', AreaListView.as_view(), name='area_list'),
    url(r'^areas/(?P<pk>\d+)/$', AreaDetailView.as_view(), name='area_detail'),
)