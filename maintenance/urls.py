from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [	
    url(r'^fix/$',login_required(FixListView.as_view()), name='fix_list'),
    url(r'^fix/add/$', login_required(FixCreateView.as_view()), name='fix_create'),
    #url(r'^brand/(?P<pk>\d+)/edit/$', login_required(BrandUpdateView.as_view()), name='brand_update'),    
]