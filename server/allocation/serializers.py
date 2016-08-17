from rest_framework import serializers
from drf_custom_fields import fields
from equipment.models import Device
from .models import *

class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation

    def create(self, validated_data):

        device = validated_data.get('device')
        assignments = Allocation.objects.filter(device=device, is_active=True)

        for assignment in assignments:
            assignment.is_active = False
            assignment.save()

        allocation = Allocation.objects.create(**validated_data)
        return allocation
