from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

from django.views.generic import TemplateView

urlpatterns = [	
    url(r'^reports/$',login_required(TemplateView.as_view(template_name='reporting/index.html')), name='reporting_home'),
    url(r'^reporting/equipments/$', equipment_report, name='report_equipments'),
    #url(r'^brand/add/$', login_required(BrandCreateView.as_view()), name='brand_create'),
    url(r'^dispatch/(?P<pk>\d+)/print/$', login_required(DispatchPrintView.as_view()), name='dispatch_print'),
    #url(r'^brand/(?P<pk>\d+)/delete/$', login_required(BrandDeleteView.as_view()), name='brand_delete'),
]