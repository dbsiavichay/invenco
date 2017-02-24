from django.conf.urls import url
from .views import *

urlpatterns = [	
    url(r'^brand/$', BrandListView.as_view(), name='brand_list'),
    url(r'^brand/add/$', BrandCreateView.as_view(), name='brand_create'),
    url(r'^brand/(?P<pk>\d+)/edit/$', BrandUpdateView.as_view(), name='brand_update'),
    url(r'^brand/(?P<pk>\d+)/delete/$', BrandDeleteView.as_view(), name='brand_delete'),
    url(r'^type/$', TypeListView.as_view(), name='type_list'),
    url(r'^type/add/$', TypeCreateView.as_view(), name='type_create'),
    url(r'^type/(?P<pk>\d+)/edit/$', TypeUpdateView.as_view(), name='type_update'),
    url(r'^type/(?P<pk>\d+)/delete/$', TypeDeleteView.as_view(), name='type_delete'),
    url(r'^set/$', SetListView.as_view(), name='set_list'),
    url(r'^set/add/$', SetCreateView.as_view(), name='set_create'),
    url(r'^set/(?P<pk>\d+)/edit/$', SetUpdateView.as_view(), name='set_update'),
    url(r'^model/$', ModelListView.as_view(), name='model_list'),    
    url(r'^model/add/select-type/$', SelectTypeListView.as_view(), name='model_select_type'),
    url(r'^model/add/type/(?P<type>\d+)/$', ModelCreateView.as_view(), name='model_create'),
    url(r'^model/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', ModelUpdateView.as_view(), name='model_update'),
    url(r'^model/(?P<pk>\d+)/delete/$', ModelDeleteView.as_view(), name='model_delete'),
    url(r'^equipment/$', EquipmentListView.as_view(), name='equipment_list'),
    url(r'^equipment/add/select-type/$', SelectTypeListView.as_view(), name='equipment_select_type'),
    url(r'^equipment/add/type/(?P<type>\d+)/$', EquipmentCreateView.as_view(), name='equipment_create_by_type'),
    url(r'^equipment/add/set/(?P<set>\d+)/$', EquipmentCreateView.as_view(), name='equipment_create_by_set'),
    url(r'^equipment/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', EquipmentUpdateView.as_view(), name='equipment_update_by_type'),
    url(r'^equipment/set/(?P<pk>\d+)/edit/$', EquipmentUpdateView.as_view(), name='equipment_update_by_set'),
]