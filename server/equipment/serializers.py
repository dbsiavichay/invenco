from rest_framework import serializers
from .models import Trademark, Type, TypeSpecification

class TrademarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trademark
        fields = ('id','name',)

class TypeSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSpecification
        fields = ('id', 'name', 'when', 'options')

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
