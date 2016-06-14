from rest_framework import serializers
from .models import Trademark

class TrademarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trademark
        fields = ('id','name',)
