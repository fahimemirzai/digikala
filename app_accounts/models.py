from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator  # @@@@@@@@@@@
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
import datetime
import jdatetime
from .validation import validate_order_number, validate_mailing_code, validate_cellphone, \
    validate_national_code  # @@@@


# class ActiveUser(models.Model):
#    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
#    active_code=models.CharField(max_length=5,null=True,blank=True)
#    active=models.BooleanField(default=False,null=True,blank=True)
#    active-user_name=models.CharField(max_length=10,null=True,blank=True)


class BasketItem(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=True)
    count = models.PositiveSmallIntegerField(default=0)  # 111111111111111111111111111111
    price = models.PositiveIntegerField(null=True, blank=True, default=0)  # (تعداد*هزینه هرکدوم)==
    discount = models.PositiveIntegerField(default=0, null=True)

    @property
    def discount_price(self):
        return self.price - self.discount

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True)  # app_label-->model-->id(id mahsol)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True,
                                blank=True)  # 222222222222222222222222222222 SET_NULL
    STATUS = (('active', 'active'), ('favorites', 'favorites'), ('pardakht', 'pardakht'),
              ('pardakht-shod', 'pardakht-shod'), ('canceled', 'canceled'))
    status = models.CharField(max_length=30, choices=STATUS, null=True, )
    delivered = models.BooleanField(null=True, default=False) # 111111111111111111111111111111
    order_number = models.CharField(max_length=13, validators=[MinLengthValidator(13),
                                                               validate_order_number], null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0, null=True)
    total_discount = models.PositiveIntegerField(default=0, null=True)
    total_discount_price = models.PositiveIntegerField(default=0, null=True)

    @property   # 222222222222222222222222222222
    def payable_amount(self):
        if self.total_price == 0:
            return None # 222222222222222222222222222222

        elif self.total_discount_price >= 200:
            return self.total_discount_price
        else:
            return self.total_discount_price + 9.5

    @property
    def shipping_cost(self):
        # if self.total_price==None:
        #     return None
        if self.total_discount_price >= 200:
            return 0
        elif self.total_discount_price==0:
            return None
        else:
            return 9.5

    order_registration_date = models.DateField(null=True, blank=True)
    deliverydate = models.ForeignKey('DeliveryDate', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(null=True, blank=True, default=False)
    POSITION = (('1', 'اماده سازی سفارش'), ('2', 'خروج  از مرکز پردازش'),
                ('3', 'دریافت در مرکز توزیع'), ('4', 'تحویل به مامور ارسال'), ('5', 'تحویل مرسوله به مشتری'))
    position = models.CharField(max_length=1, null=True, blank=True, choices=POSITION)

    @property
    def order_registration_date_jalali(self):
        if self.order_registration_date:
            m_date = self.order_registration_date
            jdate = jdatetime.date.fromgregorian(year=m_date.year, month=m_date.month, day=m_date.day)
            return str(jdate) #@@@@@@@@


class DeliveryDate(models.Model):
    date = models.DateField(null=True, blank=True)
    TIME_RANGE = (('A', '9-12'), ('B', '12-3'), ('C', '3-6'), ('D', '6-9'))
    time_range = models.CharField(max_length=10, choices=TIME_RANGE, null=True, blank=True)
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(50)], null=True, blank=True, default=0)

    @property
    def available(self):
        if self.capacity >= 50:
            return False
        elif self.capacity < 50:
            return True

    @property
    def date_jalali(self):
        if self.date:
            j_date = jdatetime.date.fromgregorian(year=self.date.year, month=self.date.month, day=self.date.day)
            return str(j_date)

    @property
    def range_time(self):
        return dict(self.TIME_RANGE)[self.time_range]  # @@@@@@@@@@@@@@@@@@@@@@@


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _birth_date = models.DateField(null=True, blank=True)
    bank_card = models.CharField(max_length=16, validators=[MinLengthValidator(16)], null=True,
                                 blank=True)  # 111111111111111111111111111111
    foreign_national = models.BooleanField(default=False)
    newsletter_receive = models.BooleanField(default=False, null=True, blank=True)
    national_code = models.CharField(max_length=10, validators=[MinLengthValidator(10),
                                                                validate_national_code], null=True, blank=True)

    @property
    def birth_date_jalali(self):
        if self._birth_date:
            j_date = jdatetime.date.fromgregorian(year=self._birth_date.year, month=self._birth_date.month,
                                                  day=self._birth_date.day)  # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            return str(j_date)
        else:
            return None

    @birth_date_jalali.setter  ###################################################
    def birth_date_jalali(self, value):
        dt = value.split('-')
        year = int(dt[0])
        month = int(dt[1])
        day = int(dt[2])
        gre = jdatetime.date(year, month, day).togregorian()  ###################################################
        self._birth_date = gre

    def save(self, *args, **kwargs):  # کل این تابع ???????????????????????????????????????????????????????

        if self._state.adding is True:  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ self._state.adding is True=for create
            super(Profile, self).save(*args, **kwargs)

        elif self._state.adding is False:  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ self._state.adding is False=for update

            if self.foreign_national == False and bool(self.national_code) == False:
                # return self
                raise ValidationError('yeki az do "foreign_national" , "national_code" mitavanad False bashad  ')
            elif self.foreign_national == True and bool(self.national_code) == True:
                raise ValidationError('yeki az do "foreign_national" , "national_code" mitavanad True bashad')
                # return self
            else:
                super(Profile, self).save(*args, **kwargs)  # ==super().save(*args,**kwargs) فکر کنم

    def __str__(self):
        return self.user.username


class ValidationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    validation_code = models.CharField(max_length=4, validators=[MinLengthValidator(4)], null=True)


def create_profile(sender, **kwargs):  # ??????????????????????????????????
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


def delete_user(sender, instance, **kwargs):  # ??????????????????????????????????
    instance.user.delete()


post_save.connect(create_profile, sender=User)  # ??????????????????????????????????
post_delete.connect(delete_user, sender=Profile)  # ??????????????????????????????????


class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lat = models.FloatField(null=True, default=35.811777)  # latitute
    lng = models.FloatField(null=True, default=50.905918)  # longitute
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    mailing_address = models.TextField(max_length=2000, null=True)
    number = models.PositiveIntegerField(null=True)
    unit = models.PositiveIntegerField(null=True, blank=True)
    mailing_code = models.CharField(max_length=10, null=True,
                                    validators=[MinLengthValidator(10), validate_mailing_code])
    reciver = models.BooleanField(default=False)
    reciver_first_name = models.CharField(max_length=100, null=True)
    reciver_last_name = models.CharField(max_length=100, null=True)
    reciver_cellphone = models.CharField(max_length=11, validators=[MinLengthValidator(11),
                                                                    validate_cellphone], null=True)
    reciver_national_code = models.CharField(max_length=10, validators=[MinLengthValidator(10),
                                                                        validate_national_code], null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    OFFER = (('Y', 'Yes'), ('N', 'No'), ('S', 'so-so'))
    offer = models.CharField(max_length=1, choices=OFFER, null=True, blank=True)
    write_date = models.DateField(null=True,auto_now=True)  # @@@@@@@@@@@@@@@
    title = models.CharField(max_length=100, null=True, blank=True)
    viewpoint = models.TextField(max_length=2000, null=True)
    buyer = models.BooleanField(null=True, default=False)
    publish = models.BooleanField(null=True, default=False)
    STAR = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))
    star = models.CharField(max_length=1, choices=STAR, null=True, default="3")
    count_like = models.PositiveIntegerField(null=True, default=0)
    count_dislike = models.PositiveIntegerField(null=True, default=0)
    # tt= ListField(null=True,blank=True)

    @property
    def most_liked(self):
        difference = self.count_like - self.count_dislike
        return difference

    @property
    def write_date_jalali(self):
        j_date = jdatetime.date.fromgregorian(year=self.write_date.year, month=self.write_date.month,
                                              day=self.write_date.day)
        return str(j_date)


class GoodBadPoint(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    POINT = (("good", "goodpoint"), ("bad", "badpoint"))
    point = models.CharField(null=True, max_length=10, choices=POINT, default='good')
    item = models.CharField(null=True, max_length=200)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, models.CASCADE, null=True, blank=True)
    like = models.BooleanField(null=True, default=False)
    dislike = models.BooleanField(null=True, default=False)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if (self.like == True and self.dislike == True) or (self.like == False and self.dislike == False):
            # raise ValidationError('HAR 2 NEMITAVAND FALSE YA True bashand ba ham')
            return self
        else:
            super(Like, self).save(*args, **kwargs)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateField(null=True)
    text = models.TextField(max_length=3000, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    text = models.TextField(max_length=3000, null=True)
    buyer = models.BooleanField(default=False, null=True)

    count_like = models.PositiveIntegerField(null=True, default=0)
    count_dislike = models.PositiveIntegerField(null=True, default=0)
    posted_date = models.DateField(null=True)


class ReturningItem(models.Model):
    basket_item = models.ForeignKey('BasketItem', on_delete=models.CASCADE, null=True)
    returning_basket = models.ForeignKey('ReturningBasket', on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(null=True, default=0)
    purchase_amount = models.PositiveIntegerField(null=True, default=0)

    REASON = (
    ('1', 'سفارش به صورت کامل ارسال نشده'), ('2', 'سایز کالا مناسب نیست'), ('3', 'کالای غیر اصل دریافت کرده ام'),
    ('4', 'کالای دیگری ارسال شده است'), ('5', 'از خرید خود منصرف شدم'), ('6', 'رنگ کالای ارسال شده مغایرت دارد'),
    ('7', 'کالا با اطلاعات درج شده در سایت مغایرت دارد'), ('8', 'کالا ایراد ظاهری یا شکستگی دارد'),
    ('9', 'کارت گارانتی ارسال نشده'))
    reason = models.CharField(max_length=1, choices=REASON, null=True)
    descriptions = models.TextField(max_length=3000, null=True)
    # image = models.ImageField(null=True, blank=True, upload_to='app_product/images')
    STATUS = (("active", "active"), ("canceled", "canceled"), ("accepted", "accepted"), ("received", "received"))
    status = models.CharField(max_length=10, choices=STATUS, null=True)


class ReturningBasket(models.Model):
    returning_date = models.ForeignKey('ReturningDate', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=True)

    STATUS = (("active", "active"), ("canceled", "canceled"), ("accepted", "accepted"), ("received", "received"))
    status = models.CharField(max_length=10, choices=STATUS, null=True)
    registration_date = models.DateField(null=True)

    # refund_amount=models.OneToOneField('RefundAmount',on_delete=models.SET_NULL,null=True,blank=True)

    @property
    def registration_date_jalali(self):
        return jdatetime.date.fromgregorian(year=self.registration_date.year, month=self.registration_date.month,
                                            day=self.registration_date.day)


class ReturningDate(models.Model):
    returning_date = models.DateField(null=True, blank=True)

    TIME_RANGE = (("A", "9-14"), ("B", "14-8"))
    time_range = models.CharField(max_length=1, choices=TIME_RANGE, null=True, blank=True)
    capacity = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(50)], default=0)

    @property
    def available(self):
        if self.capacity >= 50:
            return False
        else:
            return True

    @property
    def range_time(self):
        return dict(self.TIME_RANGE)[self.time_range]

    @property
    def returning_date_jalali(self):
        if self.returning_date:
            m_date = self.returning_date
            j_date = jdatetime.date.fromgregorian(year=m_date.year, month=m_date.month, day=m_date.day)
            return str(j_date)


class RefundAmount(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True)
    STATUS = (('C', 'canceled'), ('R', 'returned'))
    status = models.CharField(max_length=1, choices=STATUS, null=True)

    paid = models.BooleanField(default=False, null=True)
    amount = models.PositiveIntegerField(null=True, blank=True, default=0)
