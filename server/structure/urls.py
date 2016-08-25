from rest_framework import routers
from .views	import *


structure_router = routers.DefaultRouter()
structure_router.register(r'departments', DepartmentViewSet)
structure_router.register(r'sections', SectionViewSet)
structure_router.register(r'employees', EmployeeViewSet)
