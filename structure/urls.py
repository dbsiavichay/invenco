from django.conf.urls import patterns, url
from .views	import jobs, job

urlpatterns = patterns('',
    url(r'^jobs/$', jobs, name='jobs'),
    url(r'^jobs/(?P<job_id>\d+)/$', job, name='job_detail'),
    #url(r'^albums/(?P<artist>[\w\-]+)/$', AlbumListView.as_view(), name='album_list'),
    #url(r'^albums/detail/(?P<slug>[\w\-]+)/$', AlbumDetailView.as_view(), name='album_detail'),
)