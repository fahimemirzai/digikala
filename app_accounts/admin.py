from django.contrib import admin
from . import models


class BaskeItemInline(admin.TabularInline):
    model=models.BasketItem
    extra=1


@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines=[BaskeItemInline]


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


"""
@admin.register(models.BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    pass
    """



@admin.register(models.Address)
class AdressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.GoodBadPoint)
class GoodBadPointAdmin(admin.ModelAdmin):
    pass