from .models import Provider
from .serializers import ProviderSerializer
from rest_framework import viewsets

class ProviderViewSet(viewsets.ModelViewSet):
	queryset = Provider.objects.all()
	serializer_class = ProviderSerializer
