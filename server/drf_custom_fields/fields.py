from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO

class ObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        d = {'id': value.id, 'name': value.name}
        content = JSONRenderer().render(d)
        stream = BytesIO(content)
        return JSONParser().parse(stream)

    def to_internal_value(self, data):
        return self.queryset.get(pk=data['id'])


class JsonField(serializers.Field):
    def to_representation(self, value):
        content = JSONRenderer().render(value)
        stream = BytesIO(content)
        return JSONParser().parse(stream)

    def to_internal_value(self, data):
        return data
