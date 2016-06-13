from django.conf.urls import patterns, url
from .views	import ProviderListView, ProviderDetailView

urlpatterns = patterns('',
    url(r'^providers/$', ProviderListView.as_view(), name='provider_list'),
    url(r'^providers/(?P<pk>\d+)/$', ProviderDetailView.as_view(), name='provider_detail'),    
)