from django.conf.urls import patterns, url
from .views	import TrademarkListView, TrademarkDetailView

urlpatterns = patterns('',
    url(r'^trademarks/$', TrademarkListView.as_view(), name='trademark_list'),
    url(r'^trademarks/(?P<pk>\d+)/$', TrademarkDetailView.as_view(), name='trademark_detail'),    
)