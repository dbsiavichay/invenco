from rest_framework import serializers
from drf_custom_fields import fields
from .models import Trademark, Type, TypeSpecification, Model, Device
from purchases.models import Provider

class TrademarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trademark
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
    trademark = serializers.StringRelatedField()

    class Meta:
        model = Model
        fields = ('id', 'name', 'part_number', 'type', 'trademark',)

class ModelSerializer(serializers.ModelSerializer):
    #type = fields.ObjectRelatedField(queryset=Type.objects.all())
    #trademark = fields.ObjectRelatedField(queryset=Trademark.objects.all())
    specifications = fields.JsonField()

    class Meta:
        model = Model
        fields = ('id', 'name', 'part_number', 'specifications', 'type', 'trademark',)

class DeviceListSerializer(serializers.ModelSerializer):
    specifications = fields.JsonField()
    model = serializers.StringRelatedField()
    type = serializers.SerializerMethodField()
    trademark = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ('id','model', 'type', 'trademark','code', 'serial', 'specifications', 'state',
        'provider', 'invoice', 'date_purchase', 'date_warranty', 'observation')

    def get_type(self, obj):
        return obj.model.type.name

    def get_trademark(self, obj):
        return obj.model.trademark.name

class DeviceSerializer(serializers.ModelSerializer):
    specifications = fields.JsonField()
    model = ModelListSerializer()

    class Meta:
        model = Device
        fields = ('id','model', 'code', 'serial', 'specifications', 'state',
        'provider', 'invoice', 'date_purchase', 'date_warranty', 'observation')
