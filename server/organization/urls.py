from django.conf.urls import patterns, url
from rest_framework import routers
from .views	import *


urlpatterns = patterns('',
    url(r'^sections/$', SectionListView.as_view(), name='section_list'),
    url(r'^employees/$', EmployeeListView.as_view(), name='employee_list'),
)


organization_router = routers.DefaultRouter()
organization_router.register(r'departments', DepartmentViewSet)
organization_router.register(r'sections', SectionViewSet)
organization_router.register(r'employees', EmployeeViewSet)
