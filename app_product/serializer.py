from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Cellphone
from app_accounts.models import Comment
from django.contrib.contenttypes.models import ContentType

class CellphoneSerializer(ModelSerializer):
    average_star = serializers.SerializerMethodField()
    def get_average_star(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       count=obj.coments.all().count()
       comments=obj.coments.all()
       total=0
       if count==0:
           return 2.5
       else:
           for comment in comments:
               total+=int(comment.star)

           return total/count

    class Meta:
        model = Cellphone
        fields = '__all__'





class SearchSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1000)
    price=serializers.IntegerField()


'''
class CellphoneSerializer_2(ModelSerializer):
    cellphone_image = serializers.RelatedField(source='models.Album', read_only=True)

    class Meta:
        model = models.Cellphone
        fields = ('id', 'cellphone_image')'''
