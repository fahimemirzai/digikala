from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from app_accounts.models import BasketItem,Comment,Question
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings



class SearchManager(models.Manager):#همش@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # def get_queryset(self):
    #     return super().get_queryset().filter(.....)

    def search(self, query=None):
        qs = self.get_queryset() #@@@@@@@@@@@@@@@@@@@@@@@@@@==Cellphone.sm.all()
        # import ipdb; ipdb.set_trace()
        if query is not None:
            or_lookup = (Q(name__icontains=query) #|
                         # Q(description__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs


class BaseProduct(models.Model):
    name = models.CharField(max_length=200)
    stock=models.PositiveIntegerField(default=1)
    price=models.PositiveIntegerField(default=0,null=True,blank=True)#

    basket_items = GenericRelation(BasketItem,related_query_name='basket_items')
    comments = GenericRelation(Comment)
    question=GenericRelation(Question,related_query_name='question')
    cause_cancalation=GenericRelation('CauseOfCancalation')
    video=GenericRelation('Video')
    photo=GenericRelation('Photo')

    class Meta:
        abstract = True


class BaseDigitalProduct(BaseProduct):
    scren_size = models.CharField(max_length=200, null=True, blank=True)
    resolution = models.CharField(max_length=200, null=True, blank=True)
    bluetooth = models.CharField(max_length=200, null=True, blank=True)
    camera = models.CharField(max_length=200, null=True, blank=True)
    wifi = models.CharField(max_length=200, null=True, blank=True)
    dimensions = models.CharField(max_length=200, null=True, blank=True, help_text='ابعاد')
    weight = models.CharField(max_length=200, null=True, blank=True)
    OS_description = models.CharField(max_length=200, null=True, blank=True)
    other_description = models.TextField(max_length=5000, null=True, blank=True)

    class Meta:
        abstract = True


class BasePortableDigitalProduct(BaseDigitalProduct):
    RAM = models.CharField(max_length=200, null=True, blank=True)
    internal_memory = models.CharField(max_length=200, null=True, blank=True)
    GPU = models.CharField(max_length=200, null=True, blank=True, help_text='پردازنده گرافیکی')
    operation_system = models.CharField(max_length=200, null=True, blank=True)
    touch_screen = models.CharField(max_length=200, null=True, blank=True)
    cpu_manufacture = models.CharField(max_length=200, null=True, blank=True)
    central_processor = models.CharField(max_length=200, null=True, blank=True)
    central_processor_frequency = models.CharField(max_length=200, null=True, blank=True)
    battery_charging = models.CharField(max_length=200, null=True, blank=True)
    battery_item_description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class Cellphone(BasePortableDigitalProduct):
    SIM_card_description = models.CharField(max_length=200, null=True, blank=True)
    body_structure = models.TextField(max_length=4000, null=True, blank=True)
    specific_property = models.CharField(max_length=200, null=True, blank=True)
    SIM_card_number = models.CharField(max_length=200, null=True, blank=True, help_text='تعداد سیم کارت ')
    memory_card_support = models.CharField(max_length=200, null=True, blank=True)
    maximum_memory_card_capacity = models.CharField(max_length=200, null=True, blank=True)
    colorful_screen = models.CharField(max_length=200, null=True, blank=True)
    technology = models.CharField(max_length=200, null=True, blank=True)
    pixel_density = models.CharField(max_length=200, null=True, blank=True, help_text='تراکم پیکسلی')
    protection = models.CharField(max_length=200, null=True, blank=True)
    number_of_colors = models.CharField(max_length=200, null=True, blank=True)
    communication_network = models.CharField(max_length=200, null=True, blank=True)
    network_2G = models.CharField(max_length=200, null=True, blank=True)
    network_3G = models.CharField(max_length=200, null=True, blank=True)
    network_4G = models.CharField(max_length=200, null=True, blank=True)
    communication_technology = models.CharField(max_length=200, null=True, blank=True)
    radio = models.CharField(max_length=200, null=True, blank=True)
    location_technology = models.CharField(max_length=200, null=True, blank=True)
    port = models.CharField(max_length=200, null=True, blank=True, help_text='درگاه ارتباطی')
    photo_resolution = models.CharField(max_length=200, null=True, blank=True)
    camera_capabilities = models.TextField(max_length=4000, null=True, blank=True)
    filming = models.TextField(max_length=4000, null=True, blank=True)
    selfia_camera = models.TextField(max_length=4000, null=True, blank=True)
    speaker = models.CharField(max_length=200, null=True, blank=True)
    sound_output = models.CharField(max_length=200, null=True, blank=True)
    additional_sound_description = models.TextField(max_length=4000, null=True, blank=True)
    persian_language_support = models.CharField(max_length=200, null=True, blank=True)
    software_ability = models.TextField(max_length=4000, null=True, blank=True)
    voice_recorder = models.CharField(max_length=200, null=True, blank=True)
    sensor = models.TextField(max_length=4000, null=True, blank=True)
    battery_specifications = models.TextField(max_length=5000, null=True, blank=True)
    conversation_charging_rate = models.CharField(max_length=200, null=True, blank=True, help_text='میزان شارژ مکالمه')
    cell_phone_items = models.CharField(max_length=200, null=True, blank=True)

    sm=SearchManager()
    objects = models.Manager()





class Laptop(BasePortableDigitalProduct):
    pass


class Tablet(BasePortableDigitalProduct):

    pass


class Television(BaseDigitalProduct):
    brand=models.CharField(max_length=1000,null=True)
    sm = SearchManager()
    objects = models.Manager()

    


class Photo(models.Model):
    image = models.ImageField(null=True,blank=True, upload_to='app_product/images',
                                          default='Images/None/No-img.jpg')#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    @property
    def image_url(self):
        return settings.DOMAIN+ settings.MEDIA_URL+str(self.image)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id=models.PositiveIntegerField(null=True)
    content_object=GenericForeignKey('content_type','object_id')


class Video(models.Model):

    video = models.FileField(null=True, blank=True, upload_to='app_product/videos', default='videos/None/No-img.pdf') #@@@@@@@@@@@@@@@@@@@@@@@@@@
    @property
    def video_url(self):
        return settings.DOMAIN+ settings.MEDIA_URL+str(self.image)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id=models.PositiveIntegerField(null=True)
    content_object=GenericForeignKey('content_type','object_id')




class CauseOfCancalation(models.Model):
    REASON=(("A","از خرید منصرف شده ام"),("B","میخواهم کالای خود را ویرایش کنم"),
            ("C","کد تخفیف اعمال نشده"),("D","سفارش تکراری ثبت کرده ام"),("E","قیمت کالا زیاد است"),
            ("F","هزینه ارسال زیاد است"),("G","میخواهم شیوه پرداخت را تغییر بدهم"))
    reason=models.CharField(max_length=1,null=True,blank=True)
    count=models.PositiveIntegerField(default=0,null=True,)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id=models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')



