from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator,MinLengthValidator#@@@@@@@@@@@
from django.db.models.signals import post_save,post_delete
# from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
import datetime





# class ActiveUser(models.Model):
#    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
#    active_code=models.CharField(max_length=5,null=True,blank=True)
#    active=models.BooleanField(default=False,null=True,blank=True)
#    active-user_name=models.CharField(max_length=10,null=True,blank=True)



class BasketItem(models.Model):
     basket=models.ForeignKey('Basket',on_delete=models.CASCADE,null=True)
     count = models.PositiveSmallIntegerField(default=0)
     price=models.PositiveIntegerField(null=True,blank=True,default=0) # (تعداد*هزینه هرکدوم)==
     discount=models.PositiveIntegerField(default=0,null=True)
     @property
     def discount_price(self):
         return self.price - self.discount


     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True) #app_label-->model-->id(id mahsole)
     object_id = models.PositiveIntegerField(null=True)
     content_object = GenericForeignKey('content_type', 'object_id')

def validate_order_number(value):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    if value.startswith('DKC-'):
        return value
    else:
        raise ValidationError


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.ForeignKey('Address',on_delete=models.CASCADE,null=True,blank=True)

    STATUS = (('active', 'active'),('favorites','favorites'),('pardakht','pardakht'),
              ('pardakht-shod','pardakht-shod'),('canceled','canceled'),)

    delivered=models.BooleanField(null=True,default=False)
    status=models.CharField(max_length=30, choices=STATUS, null=True,)
    order_number=models.CharField(max_length=13,validators=[MinLengthValidator(13),
                                                            validate_order_number],null=True,blank=True)#@@@@@@@@@@@@@@@@@@@@@@@@@
    total_price = models.PositiveIntegerField(default=0,null=True)
    total_discount = models.PositiveIntegerField(default=0,null=True)
    total_discount_price = models.PositiveIntegerField(default=0,null=True)

    @property #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def payable_amount(self):
        if self.total_price==0 :
            return None

        elif self.total_discount_price >= 200:
            return self.total_discount_price
        else:
            return self.total_discount_price+9.5

    @property
    def shipping_cost(self):
        # if self.total_price==None:
        #     return None
        # import ipdb; ipdb.set_trace()
        if self.total_discount_price >= 200:
            return 0
        else:
            return 9.5

    order_registration_date=models.DateField(null=True,blank=True)
    deliverydate=models.ForeignKey('DeliveryDate',on_delete=models.CASCADE,null=True,blank=True)
    active=models.BooleanField(null=True,blank=True,default=False)
    POSITION=(('1','اماده سازی سفارش'),('2','خروج  از مرکز پردازش'),
              ('3','دریافت در مرکز توزیع'),('4','تحویل به مامور ارسال'),('5','تحویل مرسوله به مشتری'))
    position=models.CharField(max_length=1,null=True,blank=True,choices=POSITION)



class DeliveryDate(models.Model):
    date=models.DateField(null=True,blank=True)
    TIME_RANGE=(('A','9-12'),('B','12-3'),('C','3-6'),('D','6-9'))
    time_range=models.CharField(max_length=10,choices=TIME_RANGE,null=True,blank=True)
    capacity=models.PositiveIntegerField(validators=[MaxValueValidator(50)],null=True,blank=True,default=0)

    @property#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def available(self):
        if self.capacity >= 50:
            return False
        elif self.capacity < 50:
            return True





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
    birth_date = models.DateField(null=True, blank=True)
    bank_kard=models.CharField(max_length=16,validators=[MinLengthValidator(16)],null=True,blank=True) #@@@@@@@@@@@@@@@
    foreign_national=models.BooleanField(default=False)
    newsletter_receive=models.BooleanField(default=False,null=True,blank=True)
    national_code = models.CharField(max_length=10,validators=[MinLengthValidator(10),
                                                               validate_national_code],null=True,blank=True)

    def save(self, *args, **kwargs):#کل این تابع ???????????????????????????????????????????????????????
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


def create_profile(sender,**kwargs): #??????????????????????????????????
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

def delete_user(sender,instance,**kwargs): #??????????????????????????????????
   instance.user.delete()

post_save.connect(create_profile,sender=User) #??????????????????????????????????
post_delete.connect(delete_user,sender=Profile) #??????????????????????????????????



def validate_mailing_code(value):
    if value.isdigit():
        return value
    else:
        raise ValidationError('must be all digit')

def validate_cellphone(value):
    if value.startswith('09'):
        return value
    else:
        raise ValidationError('must start with 09')#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


class Address(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)

    lat = models.FloatField(null=True, default=35.811777)#latitute
    lng = models.FloatField(null=True, default=50.905918)#longitute

    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    mailing_address = models.TextField(max_length=2000,null=True)
    number = models.PositiveIntegerField(null=True)
    unit = models.PositiveIntegerField(null=True, blank=True)
    mailing_code=models.CharField(max_length=10,null=True,validators=[MinLengthValidator(10),
                                                                      validate_mailing_code ])

    reciver=models.BooleanField(default=False)
    reciver_first_name=models.CharField(max_length=100,null=True)
    reciver_last_name = models.CharField(max_length=100, null=True)
    reciver_cellphone=models.CharField(max_length=11,validators=[MinLengthValidator(11),
                                                                 validate_cellphone], null=True)
    reciver_national_code = models.CharField(max_length=10,validators=[MinLengthValidator(10),
                                                            validate_national_code], null=True)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@





class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    OFFER=(('Y','Yes'),('N','No'),('S','so-so'))
    offer=models.CharField(max_length=1,choices=OFFER,null=True,blank=True)
    write_date=models.DateField(null=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    viewpoint=models.TextField(max_length=2000,null=True)
    # strengths=models.TextField(max_length=1000,null=True,blank=True)
    # weak_points=models.TextField(max_length=1000,null=True,blank=True)
    buyer=models.BooleanField(null=True,default=False)
    publish=models.BooleanField(null=True,default=False)
    STAR=(("1","1"),("2","2"),("3","3"),("4","4"),("5","5"))
    star=models.CharField(max_length=1,choices=STAR,null=True,default="3")
    count_like = models.PositiveIntegerField(null=True, default=0)
    count_dislike = models.PositiveIntegerField(null=True, default=0)

    @property
    def most_liked(self):
        difference=self.count_like - self.count_dislike
        return difference

    # tt= ListField(null=True,blank=True)

class GoodBadPoint(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    POINT=(("good","goodpoint"),("bad","badpoint"))
    point=models.CharField(null=True,max_length=10,choices=POINT,default='good')
    item=models.CharField(null=True,max_length=200)



class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,models.CASCADE,null=True,blank=True)
    like=models.BooleanField(null=True,default=False)
    dislike = models.BooleanField(null=True, default=False)
    reply=models.ForeignKey('Reply',on_delete=models.CASCADE,null=True,blank=True)

    def save(self,*args,**kwargs):
        if (self.like==True and self.dislike==True) or (self.like==False and self.dislike==False):
            # raise ValidationError('HAR 2 NEMITAVAND FALSE YA True bashand ba ham')
            return self
        else:
            super(Like, self).save(*args, **kwargs)




class Question(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    posted_date=models.DateField(null=True)
    text=models.TextField(max_length=3000,null=True)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id=models.PositiveIntegerField(null=True)
    content_object=GenericForeignKey('content_type','object_id')


class Reply(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE,blank=True)
    text=models.TextField(max_length=3000,null=True)
    buyer=models.BooleanField(default=False,null=True)

    count_like = models.PositiveIntegerField(null=True, default=0)
    count_dislike = models.PositiveIntegerField(null=True, default=0)
    posted_date = models.DateField(null=True)


class ReturningItem(models.Model):
    basket_item = models.ForeignKey('BasketItem',on_delete=models.CASCADE,null=True)
    returning_basket=models.ForeignKey('ReturningBasket',on_delete=models.CASCADE,null=True)
    count=models.PositiveIntegerField(null=True,default=0)
    purchase_amount=models.PositiveIntegerField(null=True,default=0)

    REASON=(('1','سفارش به صورت کامل ارسال نشده'),('2','سایز کالا مناسب نیست'),('3','کالای غیر اصل دریافت کرده ام'),
            ('4','کالای دیگری ارسال شده است'),('5','از خرید خود منصرف شدم'),('6','رنگ کالای ارسال شده مغایرت دارد'),
            ('7','کالا با اطلاعات درج شده در سایت مغایرت دارد'),('8','کالا ایراد ظاهری یا شکستگی دارد'),
            ('9','کارت گارانتی ارسال نشده'))
    reason=models.CharField(max_length=1,choices=REASON,null=True)
    descriptions=models.TextField(max_length=3000,null=True)
    # image = models.ImageField(null=True, blank=True, upload_to='app_product/images')
    STATUS=(("active","active"),("canceled","canceled"),("accepted","accepted"),("received","received"))
    status=models.CharField(max_length=10,choices=STATUS,null=True)



class ReturningBasket(models.Model):
    returning_date=models.ForeignKey('ReturningDate',on_delete=models.SET_NULL,null=True,blank=True)
    address=models.ForeignKey('Address',on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    basket=models.ForeignKey('Basket',on_delete=models.CASCADE,null=True)

    STATUS = (("active", "active"), ("canceled", "canceled"), ("accepted", "accepted"), ("received", "received"))
    status = models.CharField(max_length=10, choices=STATUS, null=True)
    registration_date=models.DateField(null=True)
    # refund_amount=models.OneToOneField('RefundAmount',on_delete=models.SET_NULL,null=True,blank=True)




class ReturningDate(models.Model):
    returning_date = models.DateField(null=True, blank=True)

    TIME_RANGE=(("A","9-14"),("B","14-8"))
    time_range=models.CharField(max_length=1,choices=TIME_RANGE,null=True,blank=True)
    capacity=models.PositiveIntegerField(null=True,validators=[MaxValueValidator(50)],default=0)

    @property
    def available(self):
        if self.capacity>=50:
            return False
        else:
            return True


class RefundAmount(models.Model):
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,null=True)
    STATUS=(('C','canceled'),('R','returned'))
    status=models.CharField(max_length=1,choices=STATUS,null=True)
    paid=models.BooleanField(default=False,null=True)
    amount=models.PositiveIntegerField(null=True,blank=True,default=0)
