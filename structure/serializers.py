from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('code', 'name')

class EmployeeSerializer(serializers.ModelSerializer):
    charter = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('charter', 'name')

    def get_charter(self, obj):
        return obj.contributor.charter

    def get_name(self, obj):
        return obj.contributor.name