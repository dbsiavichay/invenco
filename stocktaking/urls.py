from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [	
    url(r'^brand/$',login_required(BrandListView.as_view()), name='brand_list'),
    url(r'^brand/add/$', login_required(BrandCreateView.as_view()), name='brand_create'),
    url(r'^brand/(?P<pk>\d+)/edit/$', login_required(BrandUpdateView.as_view()), name='brand_update'),
    url(r'^brand/(?P<pk>\d+)/delete/$', login_required(BrandDeleteView.as_view()), name='brand_delete'),
    url(r'^type/$', login_required(TypeListView.as_view()), name='type_list'),
    url(r'^type/add/$', login_required(TypeCreateView.as_view()), name='type_create'),
    url(r'^type/(?P<pk>\d+)/edit/$', login_required(TypeUpdateView.as_view()), name='type_update'),
    url(r'^type/(?P<pk>\d+)/delete/$', login_required(TypeDeleteView.as_view()), name='type_delete'),
    url(r'^set/$', login_required(SetListView.as_view()), name='set_list'),
    url(r'^set/add/$', login_required(SetCreateView.as_view()), name='set_create'),
    url(r'^set/(?P<pk>\d+)/edit/$', login_required(SetUpdateView.as_view()), name='set_update'),
    url(r'^model/$', login_required(ModelListView.as_view()), name='model_list'),    
    url(r'^model/add/select-type/$', login_required(SelectTypeListView.as_view()), name='model_select_type'),
    url(r'^model/add/type/(?P<type>\d+)/$', login_required(ModelCreateView.as_view()), name='model_create'),
    url(r'^model/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', login_required(ModelUpdateView.as_view()), name='model_update'),
    url(r'^model/(?P<pk>\d+)/delete/$', login_required(ModelDeleteView.as_view()), name='model_delete'),
    url(r'^equipment/$', login_required(EquipmentListView.as_view()), name='equipment_list'),
    url(r'^equipment/add/select-type/$', login_required(SelectTypeListView.as_view()), name='equipment_select_type'),
    url(r'^equipment/add/type/(?P<type>\d+)/$', login_required(EquipmentCreateView.as_view()), name='equipment_create_by_type'),
    url(r'^equipment/add/set/(?P<set>\d+)/$', login_required(EquipmentCreateView.as_view()), name='equipment_create_by_set'),
    url(r'^equipment/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', login_required(EquipmentUpdateView.as_view()), name='equipment_update_by_type'),
    url(r'^equipment/set/(?P<pk>\d+)/edit/$', login_required(EquipmentUpdateView.as_view()), name='equipment_update_by_set'),
    url(r'^replacement/$', login_required(ReplacementListView.as_view()), name='replacement_list'),
    url(r'^replacement/add/select-type/$', login_required(SelectTypeListView.as_view()), name='replacement_select_type'),
    url(r'^replacement/add/type/(?P<pk>\d+)/$', login_required(ReplacementCreateView.as_view()), name='replacement_create'),
    url(r'^assignment/add/equipment/(?P<pk>\d+)/$', login_required(AssignmentCreateView.as_view()), name='assignment_create_by_equipment'),
    url(r'^assignment/add/set/(?P<set>\d+)/$', login_required(AssignmentCreateView.as_view()), name='assignment_create_by_equipment'),
]