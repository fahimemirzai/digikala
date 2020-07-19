from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Cellphone,Photo,Color
from app_accounts.models import Comment
from django.contrib.contenttypes.models import ContentType

class CellphoneSerializer(ModelSerializer):
    discount_percent = serializers.SerializerMethodField()
    number_of_comments=serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    number_of_voter = serializers.SerializerMethodField()
    average_vote = serializers.SerializerMethodField()
    all_image = serializers.SerializerMethodField()

    def get_discount_percent(self,obj):
        return obj.discount/obj.price

    def get_color(self,obj):
        all_colors=Color.objects.filter(object_id=obj.id,content_type=ContentType.objects.get_for_model(obj))
        ser=ColorSerializer(all_colors,many=True)
        return ser.data

    def get_number_of_voter(self,obj):
        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.id).count() #@@@@@@@@@@@@

    def get_average_vote(self,obj):
        count=Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.id).count()
        if count==0:
            return None
        else:
            comments=Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.id)
            sum=0
            for i in comments:
                sum += int(i.star)
            # import ipdb; ipdb.set_trace()
            return sum/count



    def get_all_image(self,obj):
        ct=ContentType.objects.get_for_model(obj)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        images=Photo.objects.filter(content_type=ct,object_id=obj.id)
        if bool(images):
            ser=PhotoSerializer(images,many=True)
            return ser.data
        else:
            return None

    def get_number_of_comments(self,obj):
           model=ContentType.objects.get_for_model(obj)
           return Comment.objects.filter(content_type=model,object_id=obj.id).count() #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    class Meta:
        model = Cellphone
        fields = '__all__'

class AllCellphoneSerializer(ModelSerializer):
    image=serializers.SerializerMethodField()
    color=serializers.SerializerMethodField()
    discount_percent=serializers.SerializerMethodField()
    number_of_voter=serializers.SerializerMethodField()
    average_vote=serializers.SerializerMethodField()

    def get_image(self,obj):
        if obj.photo.first():
            return obj.photo.first().image_url
        else:
            return None
    def get_color(self,obj):
        all_colors=Color.objects.filter(object_id=obj.id,content_type=ContentType.objects.get_for_model(obj))
        ser=ColorSerializer(all_colors,many=True)
        return ser.data

    def get_discount_percent(self,obj):
        return obj.discount/obj.price

    def get_number_of_voter(self,obj):
        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.id).count() #@@@@@@@@@@@@

    def get_average_vote(self,obj):
        count=Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.id).count()
        if count==0:
            return None
        else:
            comments=Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),object_id=obj.id)
            sum=0
            for i in comments:
                sum += int(i.star)
            # import ipdb; ipdb.set_trace()
            return sum/count

    class Meta:
        model=Cellphone
        fields=['name','image','color','price','discounted_price','discount_percent','number_of_voter','average_vote']



class ErrorSerializer(serializers.Serializer):
    error=serializers.SerializerMethodField()
    def get_error(self,obj):
        return 'type ra vared konid (baraye mesal)---->?type=Cellphone'


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


class ColorSerializer(ModelSerializer):
    class Meta:
        model=Color
        fields=['colors','available']