from django.conf.urls import url
from .views import *

urlpatterns = [	
    url(r'^providers/$', ProviderListView.as_view(), name='provider_list'),
    url(r'^provider/add/$', ProviderCreateView.as_view(), name='provider_create'),
    url(r'^provider/(?P<pk>\d+)/edit/$', ProviderUpdateView.as_view(), name='provider_update'),
    url(r'^provider/(?P<pk>\d+)/delete/$', ProviderDeleteView.as_view(), name='provider_delete'),

    url(r'^invoices/$', InvoiceListView.as_view(), name='invoice_list'),
    url(r'^invoice/add/$', InvoiceCreateView.as_view(), name='invoice_create'),
    url(r'^invoice/(?P<pk>\d+)/update/$', InvoiceUpdateView.as_view(), name='invoice_update'),
    #url(r'^invoice/(?P<pk>\d+)/$', InvoiceDetailView.as_view(), name='invoice_detail'),
    url(r'^invoice/(?P<pk>\d+)/equipments/$', InvoiceEquipmentsUpdateView.as_view(), name='invoice_equipments'),
]