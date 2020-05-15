from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BasketItem, Basket, Profile


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #phone = serializers.IntegerField(required=True)
    """
    token = serializers.SerializerMethodField()# چرا توکن نوشتیم؟؟؟
    def get_token(self, obj, *args, **kwargs):
        token, create = Token.objects.get_or_create(user=obj)
        return token.key
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    """
    def update(self,instance,validated_data):
        old_username=instance.username
        old_password=instance.password
        obj=super().update(instance,alidated_data)
        obj.set_username=old_username
        obj.set_password=old_password
        obj.save()
        return obj 
        """


"""
class Model_Json_Serializers(serializers.Serializer):
     id=serializers.IntegerField(required=True)
     number=serializers.IntegerField(required=True)  
"""
class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        #import ipdb ; ipdb.set_trace()
        return obj.user.email
    class Meta:
        model = Profile
        fields='__all__'


class EditProfileSerializer(serializers.ModelSerializer):
    """first_name = serializers.SerializerMethodField()
    def get_first_name(self,obj):
        user=Profile.objects.get(user=obj.user)"""
    class Meta:
        model = Profile
        fields = ('birth_date','national_code','phone_number')
        #fields='__all__'


class BasketItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField() #فقط خواندنی است
    price = serializers.SerializerMethodField()

    def get_item(self, obj, *args, **kwargs):
        return obj.content_object.name

    def get_price(self, obj, *args, **kwargs):
        return obj.content_object.price * obj.count

    class Meta:
        model = BasketItem
        fields = ('count', 'basket', 'content_type', 'price', 'item')
        #depth = 1


class BasketSerializer(serializers.ModelSerializer):
    item_list = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_item_list(self,obj): #جدید
        item = obj.basketitem_set.all()
        ser = BasketItemSerializer(item, many=True)
        return ser.data

    def get_total_price(self,obj, *args, **kwargs):
        items = obj.basketitem_set.all()
        result = 0
        for item in items:
            result += item.content_object.price * item.count#جدید
        return result

    class Meta:
        model = Basket
        fields = '__all__'
