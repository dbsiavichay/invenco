from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [	            
    url(r'^model/$', login_required(ModelListView.as_view()), name='model_list'),    
    url(r'^(?P<model>[-\w]+)/select-type/$', login_required(SelectTypeListView.as_view()), name='select_type'),
    url(r'^model/add/type/(?P<type>\d+)/$', login_required(ModelCreateView.as_view()), name='model_create'),
    url(r'^model/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', login_required(ModelUpdateView.as_view()), name='model_update'),
    url(r'^model/(?P<pk>\d+)/delete/$', login_required(ModelDeleteView.as_view()), name='model_delete'),
    url(r'^equipment/$', login_required(EquipmentListView.as_view()), name='equipment_list'),    
    url(r'^equipment/model/$', login_required(EquipmentModelListView.as_view()), name='equipment_model_list'),
    url(r'^equipment/add/select-type/$', login_required(SelectTypeListView.as_view()), name='equipment_select_type'),
    url(r'^equipment/add/type/(?P<type>\d+)/$', login_required(EquipmentCreateView.as_view()), name='equipment_create_by_type'),
    url(r'^equipment/add/set/(?P<set>\d+)/$', login_required(EquipmentCreateView.as_view()), name='equipment_create_by_set'),
    url(r'^equipment/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', login_required(EquipmentUpdateView.as_view()), name='equipment_update_by_type'),    
    url(r'^location/$', login_required(LocationListView.as_view()), name='location_list'),    
    url(r'^location/add/$', login_required(LocationCreateView.as_view()), name='location_create'),    
    url(r'^location/(?P<pk>\d+)/transfer/$', login_required(LocationTransferView.as_view()), name='location_transfer'),    
    url(r'^replacement/$', login_required(ReplacementListView.as_view()), name='replacement_list'),
    url(r'^replacement/add/select-type/$', login_required(SelectTypeListView.as_view()), name='replacement_select_type'),
    url(r'^replacement/add/type/(?P<pk>\d+)/$', login_required(ReplacementCreateView.as_view()), name='replacement_create'),
    #url(r'^assignment/add/equipment/(?P<pk>\d+)/$', login_required(AssignmentCreateView.as_view()), name='assignment_create_by_equipment'),
    #url(r'^assignment/add/set/(?P<set>\d+)/$', login_required(AssignmentCreateView.as_view()), name='assignment_create_by_set'),
    #url(r'^dispatches/$', login_required(DispatchListView.as_view()), name='dispatch_list'),
    #url(r'^dispatch/add/$', login_required(DispatchCreateView.as_view()), name='dispatch_create'),
]