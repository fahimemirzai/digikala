from django.contrib import admin
from . import models


@admin.register(models.Cellphone)
class CellphoneAdmin(admin.ModelAdmin):

    fieldsets = (
        ('General specifications', {'fields': ('scren_size', 'SIM_card_description', 'weight', 'body_structure',
                                               'specific_property', 'SIM_card_number')}),
        ('processor', {'fields': ('central_processor', 'central_processor_frequency', 'GPU', 'cpu_manufacture')}),
        ('screen', {'fields': ('colorful_screen', 'touch_screen', 'technology', 'resolution', 'pixel_density',
                               'protection', 'number_of_colors')}),
        ('memory', {'fields': ('internal_memory', 'memory_card_support', 'RAM', 'maximum_memory_card_capacity')}),
        ('connections', {'fields': ('communication_network', 'network_2G', 'network_3G', 'network_4G',
                                    'communication_technology', 'wifi', 'radio', 'bluetooth', 'location_technology',
                                    'port')}),
        ('camera', {'fields': ('camera', 'photo_resolution', 'camera_capabilities', 'filming', 'selfia_camera')}),
        ('sound', {'fields': ('speaker', 'sound_output', 'additional_sound_description')}),
        ('Software Features', {'fields': ('operation_system', 'OS_description', 'persian_language_support',
                                          'software_ability', 'voice_recorder')}),
        ('Other Features', {'fields': ('sensor', 'battery_specifications', 'battery_item_description',
                                       'battery_charging', 'conversation_charging_rate', 'cell_phone_items')}),
        ('@', {'fields': ('name', 'dimensions', 'other_description')}),
        ('#', {'fields': ('price', 'stock')})

    )

"""
@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    pass"""

