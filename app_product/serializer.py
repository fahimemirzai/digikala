from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Cellphone


class CellphoneSerializer(ModelSerializer):

    class Meta:
        model = Cellphone
        fields = '__all__'










'''
class CellphoneSerializer_2(ModelSerializer):
    cellphone_image = serializers.RelatedField(source='models.Album', read_only=True)

    class Meta:
        model = models.Cellphone
        fields = ('id', 'cellphone_image')'''
