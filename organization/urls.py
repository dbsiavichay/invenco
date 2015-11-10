from django.conf.urls import patterns, url
from .views	import SectionListView, EmployeeListView

urlpatterns = patterns('',    
    url(r'^sections/$', SectionListView.as_view(), name='section_list'),
    url(r'^employees/$', EmployeeListView.as_view(), name='employee_list'),
)