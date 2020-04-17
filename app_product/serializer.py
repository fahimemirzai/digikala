from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from . import models


class AllcellphoneSerializer(ModelSerializer):

    class Meta:
        model = models.Cellphone
        fields = '__all__'


class CellphoneSerializer(ModelSerializer):
    cellphone_image = serializers.RelatedField(source='models.Album', read_only=True)

    class Meta:
        model = models.Cellphone
        fields = ('id', 'cellphone_image')
