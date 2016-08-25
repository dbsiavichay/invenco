from rest_framework import serializers
from purchases.models import Provider
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id','name',)

class TypeSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSpecification
        fields = ('id', 'name', 'when', 'options')

class TypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name')

class TypeSerializer(serializers.ModelSerializer):
    type_specifications = TypeSpecificationSerializer(many=True)

    class Meta:
        model = Type
        fields = ('id', 'name', 'usage', 'type_specifications')

    def create(self, validated_data):
        specifications = validated_data.pop('type_specifications')
        type = Type.objects.create(**validated_data)
        for specification in specifications:
            TypeSpecification.objects.create(type=type, **specification)
        return type

    def update(self, instance, validated_data):
        specifications = validated_data.pop('type_specifications')

        instance.name = validated_data.get('name', instance.name)
        instance.usage = validated_data.get('usage', instance.usage)
        instance.save()

        TypeSpecification.objects.filter(type=instance).delete()

        for specification in specifications:
            TypeSpecification.objects.create(type=instance, **specification)

        return instance

class ModelListSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    class Meta:
        model = Model
        fields = ('id', 'name', 'part_number', 'type', 'brand',)

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'name', 'part_number', 'specifications', 'type', 'brand',)

class EquipmentListSerializer(serializers.ModelSerializer):
    model = serializers.StringRelatedField()
    type = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    responsible = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ('id','model', 'type', 'brand','code', 'serial', 'state', 'responsible')

    def get_type(self, obj):
        return obj.model.type.name

    def get_brand(self, obj):
        return obj.model.brand.name

    def get_responsible(self, obj):
        assignments = obj.assignment_set.filter(is_active=True)
        if len(assignments)>0:
            return assignments[0].responsible()
        else:
            return ''

class EquipmentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    is_assignment = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ('id','model', 'type','code', 'serial', 'specifications', 'state',
        'provider', 'invoice', 'date_purchase', 'date_warranty', 'observation', 'is_assignment')

    def get_type(self, obj):
        return obj.model.type.id

    def get_is_assignment(self, obj):
        assignments = obj.assignment_set.filter(is_active=True)
        return True if len(assignments)>0 else False

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment

    def create(self, validated_data):
        equipment = validated_data.get('equipment')
        assignments = Assignment.objects.filter(equipment=equipment, is_active=True)

        for assignment in assignments:
            assignment.is_active = False
            assignment.save()

        assignment = Assignment.objects.create(**validated_data)
        return assignment
