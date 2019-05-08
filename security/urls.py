from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'security/login.html',}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'), 
    url(
    	r'^change-password/$', auth_views.password_change, 
    	{
    		'template_name': 'security/change-password.html',
    		'post_change_redirect': '/change-password-done/'
    	}
    ), 
    url(
    	r'^change-password-done/$', auth_views.password_change_done, 
    	{
    		'template_name': 'security/change-password-done.html',
    	}
    ),  
]