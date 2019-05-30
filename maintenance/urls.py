from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [	
    url(r'^ticket/$',login_required(TicketListView.as_view()), name='ticket_list'),
    url(r'^ticket/user/$',login_required(TicketUserListView.as_view()), name='ticket_user_list'),
    url(r'^ticket/add/$', login_required(TicketCreateView.as_view()), name='ticket_create'),
    url(r'^ticket/(?P<pk>\d+)/update/$', login_required(TicketUpdateView.as_view()), name='ticket_update'),    
    url(r'^ticket/(?P<pk>\d+)/detail/$', login_required(TicketDetailView.as_view()), name='ticket_detail'),    
    url(r'^reply/ticket/(?P<pk>\d+)/solved/$', login_required(ReplySolvedCreateView.as_view()), name='reply_solved'),    
    url(r'^reply/ticket/(?P<pk>\d+)/closed/$', login_required(ReplyClosedCreateView.as_view()), name='reply_closed'),    
    url(r'^reply/ticket/(?P<pk>\d+)/canceled/$', login_required(ReplyCanceledCreateView.as_view()), name='reply_canceled'),  

    url(r'^get_component/(?P<pk>\d+)/$', login_required(get_component), name='get_component'),
]