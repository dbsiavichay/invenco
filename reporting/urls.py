from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

from django.views.generic import TemplateView

urlpatterns = [	
    url(r'^reports/$',login_required(TemplateView.as_view(template_name='reporting/index.html')), name='reporting'),
    url(r'^testreport/$', test_report, name='report'),
    #url(r'^brand/add/$', login_required(BrandCreateView.as_view()), name='brand_create'),
    #url(r'^brand/(?P<pk>\d+)/edit/$', login_required(BrandUpdateView.as_view()), name='brand_update'),
    #url(r'^brand/(?P<pk>\d+)/delete/$', login_required(BrandDeleteView.as_view()), name='brand_delete'),
]