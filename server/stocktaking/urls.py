from rest_framework import routers
from .views import *

stocktaking_router = routers.DefaultRouter()
stocktaking_router.register(r'brands', BrandViewSet)
stocktaking_router.register(r'types/list', TypeListViewSet)
stocktaking_router.register(r'types', TypeViewSet)
stocktaking_router.register(r'models/list', ModelListViewSet)
stocktaking_router.register(r'models', ModelViewSet)
stocktaking_router.register(r'equipments/list', EquipmentListViewSet)
stocktaking_router.register(r'equipments', EquipmentViewSet)
stocktaking_router.register(r'assignments', AssignmentViewSet)
