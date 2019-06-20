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

    url(r'^equipment/add/type/(?P<type>\d+)/$', login_required(EquipmentCreateView.as_view()), name='equipment_create'),
    url(r'^equipment/(?P<pk>\d+)/edit/$', login_required(EquipmentUpdateView.as_view()), name='equipment_update'),    
    url(r'^location/$', login_required(LocationListView.as_view()), name='location_list'),    
    url(r'^location/add/$', login_required(LocationCreateView.as_view()), name='location_create'),    
    url(r'^location/(?P<pk>\d+)/transfer/$', login_required(LocationTransferView.as_view()), name='location_transfer'),    
    
    url(r'^replacement/$', login_required(ReplacementListView.as_view()), name='replacement_list'),        
    url(r'^replacement/stock/$', login_required(ReplacementStockView.as_view()), name='replacement_stock'),
    url(r'^replacement/(?P<pk>\d+)/delete/$', login_required(ReplacementDeleteView.as_view()), name='replacement_delete'),
    
    url(r'^consumable/$', login_required(ConsumableListView.as_view()), name='consumable_list'),        
    url(r'^consumable/stock/$', login_required(ConsumableStockView.as_view()), name='consumable_stock'),

    url(r'^dispatch/$', login_required(DispatchListView.as_view()), name='dispatch_list'),
    url(r'^dispatch/add/$', login_required(DispatchCreateView.as_view()), name='dispatch_create'),    
    
    url(r'^get_component/(?P<pk>\d+)/$', get_component, name='consumable_select'),    
]