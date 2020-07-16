from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Cellphone,Photo
from app_accounts.models import Comment
from django.contrib.contenttypes.models import ContentType

class CellphoneSerializer(ModelSerializer):
    all_image=serializers.SerializerMethodField()
    # average_star = serializers.SerializerMethodField()
    # def get_average_star(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       # count=obj.coments.all().count()
       # comments=obj.coments.all()
       # total=0
       # if count==0:
       #     return 2.5
       # else:
       #     for comment in comments:
       #         total+=int(comment.star)
       #
       #     return total/count
    def get_all_image(self,obj):
        ct=ContentType.objects.get_for_model(obj)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        images=Photo.objects.filter(content_type=ct,object_id=obj.id)
        if bool(images):
            ser=PhotoSerializer(images,many=True)
            return ser.data
        else:
            return None

    class Meta:
        model = Cellphone
        fields = '__all__'

class AllCellphoneSerializer(ModelSerializer):
    image=serializers.SerializerMethodField()

    def get_image(self,obj):
        if obj.photo.first():
            return obj.photo.first().image_url
        else:
            return None
    class Meta:
        model=Cellphone
        fields=['name','price','image']





class SearchSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1000)
    price=serializers.IntegerField()


'''
class CellphoneSerializer_2(ModelSerializer):
    cellphone_image = serializers.RelatedField(source='models.Album', read_only=True)

    class Meta:
        model = models.Cellphone
        fields = ('id', 'cellphone_image')'''


#
# class AlbumSerializer(serializers.ModelSerializer):
#     # image=serializers.ImageField(max_length=None,use_url=True)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     # video=serializers.FileField(max_length=None,use_url=True)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
#
#     # def get_image(self, obj):
#     #     return obj.image.url
#     class Meta:
#         model=Album
#         fields=('image_url','video')

class PhotoSerializer(ModelSerializer):
    class Meta:
        model=Photo
        fields=['image_url']
        