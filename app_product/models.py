from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from app_accounts.models import BasketItem



class BaseProduct(models.Model):
    name = models.CharField(max_length=200)
    stock=models.PositiveIntegerField(default=1)
    price=models.PositiveIntegerField(default=0,null=True,blank=True)#
    basket_items = GenericRelation(BasketItem)

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




class Laptop(BasePortableDigitalProduct):
    pass


class Tablet(BasePortableDigitalProduct):

    pass


class Television(BaseDigitalProduct):

    pass

"""
class Album(models.Model):
    cellphone = models.ForeignKey(Cellphone, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True, upload_to='app_product/images')"""





