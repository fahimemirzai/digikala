from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class BasketItem(models.Model):
     basket=models.ForeignKey('Basket',on_delete=models.CASCADE,null=True)
     count = models.PositiveSmallIntegerField(default=0)

     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True) #app_label-->model-->id(id mahsole)
     object_id = models.PositiveIntegerField(null=True)
     content_object = GenericForeignKey('content_type', 'object_id')



class Basket(models.Model):
    STATUS=(('active','active'),('no active','no active'))
    status=models.CharField(max_length=15,choices=STATUS,null=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
         return self.user.username









    




