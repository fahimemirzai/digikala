from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator,MinLengthValidator#@@@@@@@@@@@
from django.db.models.signals import post_save,post_delete
# from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError



class BasketItem(models.Model):
     basket=models.ForeignKey('Basket',on_delete=models.CASCADE,null=True)
     count = models.PositiveSmallIntegerField(default=0)
     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True) #app_label-->model-->id(id mahsole)
     object_id = models.PositiveIntegerField(null=True)
     content_object = GenericForeignKey('content_type', 'object_id')

def validate_order_number(value):
    if value.startswith('DKC-'):
        return value
    else:
        raise ValidationError

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.OneToOneField('Address',on_delete=models.CASCADE,null=True)

    STATUS = (('active', 'active'),('favorites','favorites'),('pardakht','pardakht'),
              ('pardakht-shod','pardakht-shod'),('delivered','deliverd'),('canceled','canceled'),)
    status=models.CharField(max_length=30, choices=STATUS, null=True,)
    order_number=models.CharField(max_length=13,validators=[MinLengthValidator(13),
                                                            validate_order_number],null=True,blank=True)
    order_registration_date=models.DateField(null=True,blank=True)
    delivered_date=models.DateTimeField(null=True,blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    shipping_cost=models.FloatField(default=10,null=True,blank=True)


    def __str__(self):
         return self.user.username




def validate_national_code(value):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    code=value
    if len(code)!=10 or not(code.isdigit()):
         raise ValidationError("false")

    cn=int(code[9])
    number=''
    for i in range(9):
        number+=code[i]

    number=number+'00'

    number=number[::-1]
    total=0
    for i in range(10,1,-1):
      total+=i*int(number[i])

    remaining=total%11

    if remaining<2 and remaining==cn:
        return value

    elif remaining>=2 and cn==(11-remaining):
        return value

    else:
        raise ValidationError("false")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateTimeField(null=True, blank=True)
    #phone_number=models.IntegerField(null=True,validators=[MinValueValidator(10000000000),
    # MaxValueValidator(99999999999)])   #@@@@@@@@@@@@@@@@@@@@
    bank_kard=models.CharField(max_length=16,validators=[MinLengthValidator(16)],null=True,blank=True) #@@@@@@@@@@@@@@@
    foreign_national=models.BooleanField(default=False)
    newsletter_receive=models.BooleanField(default=False,null=True,blank=True)
    national_code = models.CharField(max_length=10,validators=[MinLengthValidator(10),
                                                               validate_national_code],null=True,blank=True)

    def save(self, *args, **kwargs):#کل این تابع @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # import ipdb; ipdb.set_trace()
        if self._state.adding is True:
            super(Profile, self).save(*args, **kwargs)

        elif self._state.adding is False:

            if self.foreign_national==False and bool(self.national_code)==False :
                return self
                # raise ValidationError('yeki az do "foreign_national" , "national_code" mitavanad False bashad  ')
            elif self.foreign_national==True and bool(self.national_code )==True:
                # raise  ValidationError('yeki az do "foreign_national" , "national_code" mitavanad True bashad')
                return self
            else:
                super(Profile, self).save(*args,**kwargs)# ==super().save(*args,**kwargs) فکر کنم

    def __str__(self):
        return self.user.username


def create_profile(sender,**kwargs): #@@@@@@@@@@@@@@@@@@@@@@@@

    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

def delete_user(sender,instance,**kwargs): #@@@@@@@@@@@@@@@@@@@@@@@@
   instance.user.delete()

post_save.connect(create_profile,sender=User) #@@@@@@@@@@@@@@@@@@@@@@@@
post_delete.connect(delete_user,sender=Profile) #@@@@@@@@@@@@@@@@@@@@@@@@



class Address(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)

    lat = models.FloatField(null=True, default=35.811777)#latitute
    lng = models.FloatField(null=True, default=50.905918)#longitute

    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    mailing_address = models.TextField(max_length=2000,null=True)
    number = models.PositiveIntegerField(null=True)
    unit = models.PositiveIntegerField(null=True, blank=True)
    mailing_code=models.IntegerField(null=True,validators=[MinValueValidator(1000000000),
                                                            MaxValueValidator(9999999999)])

    reciver=models.BooleanField(default=False)
    reciver_first_name=models.CharField(max_length=100,null=True)
    reciver_last_name = models.CharField(max_length=100, null=True)
    reciver_national_code = models.CharField(max_length=10, validators=[MinLengthValidator(10),
                                                                validate_national_code], null=True)
    reciver_cellphone=models.CharField(max_length=11,validators=[MinLengthValidator(11)], null=True)




class Comment(models.Model):
    user=models.ForeignKey(User,models.CASCADE,null=True)
    write_date=models.DateTimeField(null=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    viewpoint=models.TextField(max_length=2000,null=True)
    # strengths=models.TextField(max_length=1000,null=True,blank=True)
    # weak_points=models.TextField(max_length=1000,null=True,blank=True)
    buyer=models.BooleanField(null=True,default=False)
    publish=models.BooleanField(null=True,default=False)
    STAR=(("1","1"),("2","2"),("3","3"),("4","4"),("5","5"))
    star=models.CharField(max_length=1,choices=STAR,null=True,default="3")
    # like= models.PositiveIntegerField(null=True, blank=True,default=0)
    # dislike=models.PositiveIntegerField(null=True, blank=True,default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    most_liked=models.IntegerField(null=True,default=0)
    count_like=models.IntegerField(null=True,default=0)
    count_dislike=models.IntegerField(null=True,default=0)
    # tt= ListField(null=True,blank=True)

class GoodBadPoint(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    POINT=(("good","goodpoint"),("bad","badpoint"))
    point=models.CharField(null=True,blank=True,max_length=10,choices=POINT)
    item=models.CharField(null=True,blank=True,max_length=200)



class Like(models.Model):
    user=models.ForeignKey(User,models.CASCADE)
    comment=models.ForeignKey(Comment,models.CASCADE)
    like=models.BooleanField(null=True,blank=True,default=0)
    dislike = models.BooleanField(null=True, blank=True, default=0)













