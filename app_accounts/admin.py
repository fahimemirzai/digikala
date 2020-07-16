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

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass

@admin.register(models.DeliveryDate)
class DeliveryDateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReturningItem)
class ReturningItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReturningBasket)
class ReturningBasketAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReturningDate)
class ReturningDateAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RefundAmount)
class RefundAmountAdmin(admin.ModelAdmin):
    pass