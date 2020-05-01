from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation




class BasketItem(models.Model):
     basket=models.ForeignKey('Basket',on_delete=models.CASCADE,null=True)
     count = models.PositiveSmallIntegerField(default=0)
     #product = models.ForeignKey(BaseProduct,null=True, blank=True, on_delete=models.SET_NULL,)
     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
     object_id = models.PositiveIntegerField(null=True)
     content_object = GenericForeignKey('content_type', 'object_id')



class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_off=models.BooleanField(default=True)
    #basket_items = GenericRelation('BasketItem')
    #on_off=models.BooleanField(null=True)

    def __str__(self):
         return self.user.username









    




