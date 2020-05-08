from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BasketItem, Basket


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


class BasketItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField() #فقط خواندنی است
    price = serializers.SerializerMethodField()
    #total_price=

    def get_item(self, obj, *args, **kwargs):
        return obj.content_object.name

    def get_price(self, obj, *args, **kwargs):
        return obj.content_object.price
        # (obj.content_object.price)*count/
        # obj.content_object.price)*self.count/
        # obj.content_object.price)*obj.count

    class Meta:
        model = BasketItem
        fields = ('count', 'basket', 'content_type', 'price', 'item')
        #depth = 1





