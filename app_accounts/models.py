from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save


class BasketItem(models.Model):
     basket=models.ForeignKey('Basket',on_delete=models.CASCADE,null=True)
     count = models.PositiveSmallIntegerField(default=0)
     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True) #app_label-->model-->id(id mahsole)
     object_id = models.PositiveIntegerField(null=True)
     content_object = GenericForeignKey('content_type', 'object_id')


class Basket(models.Model):
    STATUS = (('active', 'active'), ('no active', 'no active'))
    status=models.CharField(max_length=15, choices=STATUS, null=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
         return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #first_name = models.CharField(max_length=50, null=True) #داره
    #last_name = models.CharField(max_length=50, null=True) #داره
    birth_date = models.DateField(null=True, blank=True)
    national_code = models.IntegerField(null=True, validators=[MinValueValidator(1000000000),
                                                            MaxValueValidator(9999999999)])
    #email = models.EmailField(max_length=50, null=True, blank=True) #داره
    phone_number=models.IntegerField(null=True,validators=[MinValueValidator(10000000000),
                                                            MaxValueValidator(99999999999)])
    def __str__(self):
        return self.user.username

def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=Profile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)


class Address(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    # AZ ON MODEL MAP HA
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    mailing_address = models.TextField(max_length=2000,null=True)
    number = models.PositiveIntegerField(null=True)
    unit = models.PositiveIntegerField(null=True, blank=True)
    mailing_code=models.IntegerField(null=True,validators=[MinValueValidator(1000000000),
                                                            MaxValueValidator(9999999999)])

    #اطلاعات گیرنده سفارش(یادته)
    #recipient=models.BooleanField()





    




