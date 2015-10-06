from django.conf.urls import patterns, url
from .views	import TrademarkListView, TrademarkDetailView, TypeListView, TypeDetailView, ModelListView, ModelDetailView

urlpatterns = patterns('',
    url(r'^trademarks/$', TrademarkListView.as_view(), name='trademark_list'),
    url(r'^trademarks/(?P<pk>\d+)/$', TrademarkDetailView.as_view(), name='trademark_detail'),
    url(r'^types/$', TypeListView.as_view(), name='type_list'),
    url(r'^types/(?P<pk>\d+)/$', TypeDetailView.as_view(), name='type_detail'),   
    url(r'^models/$', ModelListView.as_view(), name='model_list'),
    url(r'^models/(?P<pk>\d+)/$', ModelDetailView.as_view(), name='model_detail'),
)