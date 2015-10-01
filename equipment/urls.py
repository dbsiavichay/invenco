from django.conf.urls import patterns, url
from .views	import TrademarkListView, TrademarkDetailView, TypeListView, TypeDetailView

urlpatterns = patterns('',
    url(r'^trademarks/$', TrademarkListView.as_view(), name='trademark_list'),
    url(r'^trademarks/(?P<pk>\d+)/$', TrademarkDetailView.as_view(), name='trademark_detail'),
    url(r'^types/$', TypeListView.as_view(), name='type_list'),
    url(r'^types/(?P<pk>\d+)/$', TypeDetailView.as_view(), name='type_detail'),   
)