from django.contrib import admin
from . import models


class BaskeItemInline(admin.TabularInline):
    model=models.BasketItem
    extra=1


@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines=[BaskeItemInline]



"""
@admin.register(models.BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    pass
    """



