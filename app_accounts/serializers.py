from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    #username=serializers.CharField()
    class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self,validated_data):
        user=super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
"""
    def update(self,instance,alidated_data):
        old_username=instance.username
        old_password=instance.password
        obj=super().update(instance,alidated_data)
        obj.set_username=old_username
        obj.set_password=old_password
        obj.save()
        return obj """



class Model_Json_Serializers(serializers.Serializer):
     id=serializers.IntegerField(required=True)
     number=serializers.IntegerField(required=True)




