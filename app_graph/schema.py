import graphene
from graphene_django import DjangoObjectType
from graphene import Argument
from app_accounts.models import Profile,Address,Basket,BasketItem,Comment,ReturningBasket,ReturningItem,Like,\
    GoodBadPoint,DeliveryDate,RefundAmount,ValidationCode,ReturningDate

from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from app_product.models import Cellphone,CauseOfCancalation
from django.contrib.contenttypes.models import ContentType
from graphql import GraphQLError
from .permissions import IsOwner
import datetime
import jdatetime
import random
# from graphene.types import Scalar
import urllib.parse
import requests
from graphql_jwt.shortcuts import get_token

from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

#####################################################################################################
class UserType(DjangoObjectType):
    first_name=graphene.String()
    last_name=graphene.String()

    def resolve_first_name(self,info,**kwargs):
        if self.first_name:
            return self.first_name
        else:
            return 'کاربر دیجیکالا'


    def resolve_last_name(self,info,**kwargs):
        if self.last_name:
            return self.last_name
        else:
            return 'کاربر دیجیکالا'

    class Meta:
        model=User


class ProfileType(DjangoObjectType):
    birth_date_jalali=graphene.String(source='birth_date_jalali')
    # aa = graphene.String()

    # def resolve_aa(self,info,**kwargs):
    #     return 'aa'

    class Meta:
        model=Profile
        # interfaces = (graphene.relay.Node,)


class AddressType(DjangoObjectType):
    class Meta:
        model=Address
        # interfaces = (graphene.relay.Node,)


class BasketType(DjangoObjectType):
    shipping_cost=graphene.String(source='shipping_cost')
    payable_amount=graphene.String(source='payable_amount')
    comodity_count = graphene.Int()#########
    total_discount_persent=graphene.Float()
    order_registration_date_jalali=graphene.String()
    # response=graphene.Field(ResponseType)


    def resolve_comodity_count(self,info,**kwargs):
        number_in_basket=0
        for item in self.basketitem_set.all():
            number_in_basket += item.count
        return number_in_basket

    def resolve_total_discount_persent(self,info,**kwargs):
        if self.total_price >=0:
            return self.total_discount / self.total_price

    def resolve_order_registration_date_jalali(self,info,**kwargs):
        return self.order_registration_date_jalali


    class Meta:
        model=Basket
        # interfaces = (graphene.relay.Node,)




class BasketItemType(DjangoObjectType):
    discount_price=graphene.String(source='discount_price')
    item=graphene.String()
    price_one_item=graphene.Float()
    product_id=graphene.String()
    product_model=graphene.String()
    image=graphene.String()

    def resolve_item(self,info,**kwargs):
        return self.content_object.name

    def resolve_price_one_item(self,info,**kwargs):
        if self.count >0:
            return self.discount_price/self.count

    def resolve_product_id(self,info,**kwargs):
        return self.object_id

    def resolve_product_model(self, info, **kwargs):
        return self.content_type

    def resolve_image(self,info,**kwargs):
        if self.content_object.photo.first():
            return self.content_object.photo.first().image_url

    class Meta:
        model=BasketItem


class CommentType(DjangoObjectType):
    good_point=graphene.String()
    bad_point=graphene.String()
    image_url=graphene.String()
    write_date_jalali=graphene.String()

    def resolve_good_point(self,info,**kwargs):
        good_point=self.goodbadpoint_set.filter(point='good')
        good_points=''
        for i in good_point:
            good_points +=i.item+' , '
        return good_points


    def resolve_bad_point(self, info, **kwargs):
        bad_point = self.goodbadpoint_set.filter(point='bad')
        bad_points = ''
        for i in bad_point:
            bad_points += i.item + ' , '
        return bad_points


    def resolve_image_url(self,info,**kwargs):
        if self.content_object.photo.first():
            return self.content_object.photo.first().image_url

    def resolve_write_date_jalali(self,info,**kwargs):
        return self.write_date_jalali

    class Meta:
        model=Comment
        # interfaces = (graphene.relay.Node,)


class ReturningBasketType(DjangoObjectType):
    registration_date_jalali=graphene.String()

    def resolve_registration_date_jalali(self,info,**kwargs):
        return self.registration_date_jalali

    class Meta:
        model=ReturningBasket



class ReturnItemType(DjangoObjectType):
    product_id=graphene.String()
    product_model=graphene.String()
    image=graphene.String()
    item=graphene.String()

    def resolve_item(self,info,**kwargs):
        return self.basket_item.content_object.name


    def resolve_product_id(self,info,**kwargs):
        return self.basket_item.object_id

    def resolve_product_model(self,info,**kwargs):
        return self.basket_item.content_type

    def resolve_image(self,info,**kwargs):
        if self.basket_item.content_object.photo.first():
            return self.basket_item.content_object.photo.first().image_url

    class Meta:
        model=ReturningItem


class ReturningDateType(DjangoObjectType):
    returning_date_jalali=graphene.String()
    range_time=graphene.String()

    def resolve_range_time(self,info,**kwargs):
        return self.range_time

    def resolve_returning_date_jalali(self,info,**kwargs):
        return self.returning_date_jalali

    class Meta:
        model=ReturningDate



class LikeType(DjangoObjectType):
    class Meta:
        model=Like



class DeliveryDateType(DjangoObjectType):
    date_jalali=graphene.String()
    range_time=graphene.String()

    def resolve_date_jalali(self,info,**kwargs):
        return self.date_jalali

    def resolve_range_time(self, info, **kwargs):
        return self.range_time

    class Meta:
        model=DeliveryDate



class  CauseOfCancalationType(DjangoObjectType):
    cancel_reason=graphene.String()

    def resolve_cancel_reason(self,info,**kwargs):
        return self.cancel_reason

    class Meta:
        model=CauseOfCancalation


class RefundAmountType(DjangoObjectType):
    class Meta:
        model=RefundAmount


# class AllMessage(Scalar):
#     @staticmethod
#     def login_message(self,info,**kwargs):
#         return "کد اعتبارسنجی برای شما ارسال شد.ان را وارد کنید"
#         # return{"message":"کد اعتبارسنجی برای شما ارسال شد.ان را وارد کنید"}
#
#
# class AllMessage(graphene.ObjectType):
#     send_login_code=graphene.String()
#     token=graphene.String()
#
#     def resolve_send_login_code(self,info,**kwargs):
#         return "kode baray shoma ersal shod "
#         # return {"message": "کد اعتبارسنجی برای شما ارسال شد.ان را وارد کنید"}
#
#     def resolve_token(self,token):
#         return f" Token shome = {token } "


class ResponseType(graphene.ObjectType):
    response_message=graphene.String()
    # def resolve_response_message(self,message):
    #     return message



############################################### QUERY ######################################################



class Query(graphene.ObjectType):
    profile=graphene.Field(ProfileType)
    # user=graphene.Field(UserType)
    my_addresses=graphene.List(AddressType)
    activebasket=graphene.Field(BasketType)
    favoritebasket=graphene.Field(BasketType)
    my_comments=graphene.List(CommentType)
    # product_list=graphene.List(graphene.String, model=graphene.String)
    product_comments=graphene.List(CommentType,model=graphene.String(),id=graphene.ID(),order=graphene.String()) #$$$$$$$$$
    show_user_orders=graphene.List(BasketType,kind=graphene.String())
    show_user_return_orders=graphene.List(ReturningBasketType)
    show_special_order=graphene.Field(BasketType,id=graphene.ID())
    show_special_returned_order=graphene.Field(ReturningBasketType,id=graphene.ID())

    aa=graphene.String(name=graphene.Int(default_value=100))
    aa = graphene.String(name=graphene.Int(required=False))

    def resolve_aa(self,info,name,**kwargs):
        return str(name) +"kkk"




    @permissions_checker([IsAuthenticated])
    def resolve_show_special_order(self,info,id,**kwargs):
        try:
            returning_basket=ReturningBasket.objects.get(pk=id,user=info.context.user)

        except:
            raise GraphQLError("in order vojod nadarad ya motealegh be shoma nist")

        else:
            return returning_basket


    @permissions_checker([IsAuthenticated])
    def resolve_profile(self,info,**kwargs):
        # if not info.context.user.is_authenticated:
        #     return Profile.objects.none()
        # else:
        #     return Profile.objects.filter(user=info.context.user).first()
        return Profile.objects.get(user=info.context.user)


    @permissions_checker([IsAuthenticated])
    def resolve_my_addresses(self,info,**kwargs):
            return Address.objects.filter(profile__user=info.context.user)


    @permissions_checker([IsAuthenticated])
    def resolve_activebasket(self,info,**kwargs):
            return Basket.objects.get(user=info.context.user,status='active')


    @permissions_checker([IsAuthenticated])
    def resolve_favoritebasket(self,info,**kwargs):
            return Basket.objects.get(user=info.context.user, status='favorites')

    @permissions_checker([IsAuthenticated])
    def resolve_my_comments(self,info,**kwargs):
            return Comment.objects.filter(user=info.context.user)


    # def resolve_address(self,info,id,**kwargs):
    #     if info.context.user.is_authenticated:
    #         return Address.objects.get(pk=id)


    def resolve_product_comments(self,info,model,id,order='newest-comment',**kwargs):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']

        if model in MODELS:
            product_model = eval(model)
            try:
                product=product_model.objects.get(pk=id)
            except:
                raise  GraphQLError('chenin id va modeli vojode nadarad')
            ct = ContentType.objects.get(model=model.lower())
            if order=='newest-comment':
               return Comment.objects.filter(content_type=ct, object_id=id).order_by('-write_date')
            elif order=='most-liked':

                cm = Comment.objects.filter(content_type=ct, object_id=id)
                return  sorted(cm, key=lambda i: i.most_liked, reverse=True)
            elif order=='buyers':

                cm1 = Comment.objects.filter(content_type=ct, object_id=id, buyer=True)
                cm2 = Comment.objects.filter(content_type=ct, object_id=id, buyer=False)
                cm = cm1 | cm2
                return cm


    @permissions_checker([IsAuthenticated])
    def resolve_show_user_orders(self,info,kind='default',**kwargs):
        # if kind=='current':
        #     order1 = Basket.objects.filter(user=info.context.user, status='pardakht')
        #     order2 = Basket.objects.filter(user=info.context.user, status='pardakht-shod')
        #     order = order1 | order2
        #     order = order.exclude(delivered=True)
        #     return order
        #
        # elif kind=='delivered':
        #     order=Basket.objects.filter(user=info.context.user,delivered=True)
        #     return order
        #
        # elif kind=='canceled':
        #     order = Basket.objects.filter(user=info.context.user, status='canceled')
        #     return order
        #
        # if kind=='default':
        #     order=Basket.objects.filter(user=info.context.user).exclude(status='active').exclude(status='favorites').order_by('order_registration_date')[0:10]
        #     return order
        #
        # else:

        return [ResponseType(response_message="sllsllsl")]
        #     return 'error type must be in ["current","delivered","canceled","default"]'



    @permissions_checker([IsAuthenticated])
    def resolve_show_user_return_orders(self,info,**kwargs):
         return  ReturningBasket.objects.filter(user=info.context.user)


    @permissions_checker([IsAuthenticated])
    def resolve_show_special_returned_order(self,info,id,**kwargs):
        try:
            returning_order = ReturningBasket.objects.get(pk=id, user=info.context.user)
        except:
            raise GraphQLError(response_message="returning basketi ba in moshakhasat mojd nadarad---ya---motealegh be shoma nist")

        return returning_order

############################################# MUTATION- CLASS ##################################################


class DeleteAddress(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    address=graphene.Field(AddressType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,id):
        try:
           address=Address.objects.get(pk=id,profile__user=info.context.user)
        except:
            raise GraphQLError('in address vojude nadarad ---ya----in address motealegh be shoma nist')

        if address is not None:
            address.delete()

        return DeleteAddress(address=address)



class DeleteComment(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    comment=graphene.Field(CommentType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,id):
        try:
            comment=Comment.objects.get(pk=id,user=info.context.user)
        except:
            raise GraphQLError('incomment vojode nadarad --ya--motealegh be shoma nist')

        comment.delete()
        return DeleteComment(comment=comment)



class AddAddress(graphene.Mutation):
    class Arguments:
        lat=graphene.Float()
        lng=graphene.Float()
        province=graphene.String()
        city=graphene.String()
        mailing_address=graphene.String()
        number=graphene.Int()
        mailing_code=graphene.String()
        reciver=graphene.Boolean()
        reciver_first_name=graphene.String()
        reciver_last_name=graphene.String()
        reciver_cellphone=graphene.String()
        reciver_national_code=graphene.String()
        unit=graphene.Int()


    address=graphene.Field(AddressType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,lat,lng,province,city,mailing_address,number,mailing_code,reciver,reciver_first_name,
               reciver_last_name,reciver_cellphone,reciver_national_code,unit=None):

         address=Address.objects.create(
             lat=lat,lng=lng,province=province,city=city,mailing_address=mailing_address,number=number,
             mailing_code=mailing_code,reciver=reciver,reciver_first_name=reciver_first_name,
             reciver_last_name=reciver_last_name,reciver_cellphone=reciver_cellphone,
             reciver_national_code=reciver_national_code,unit=unit,profile=info.context.user.profile
         )
         return AddAddress(address=address)



class AddBasketItem(graphene.Mutation):
    class Arguments:
        obj_id=graphene.Int()
        obj_type=graphene.String()


    basket=graphene.Field(BasketType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,obj_id,obj_type):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        if not(obj_type in MODELS):
            raise GraphQLError('obj_type motabar nist')

        model=eval(obj_type)
        try:
            product=model.objects.get(pk=obj_id)
        except:
            raise GraphQLError('mahsouli ba in moshakhasat vojd nadarad')

        if product.stock<=0:
            raise GraphQLError("OVER PRODUCT STOCK")

        basket, created = Basket.objects.get_or_create(user=info.context.user, status='active')
        ct = ContentType.objects.get(model=obj_type.lower())
        basket_item, created = basket.basketitem_set.get_or_create(content_type=ct, object_id=obj_id)
        if basket_item.count >= product.stock:
            raise GraphQLError("OVER PRODUCT STOCK ")

        basket_item.count += 1
        basket_item.price += product.price
        basket_item.discount += product.discount
        basket_item.save()

        basket.total_price += product.price
        basket.total_discount += product.discount
        basket.total_discount_price += (product.price - product.discount)
        basket.save()

        return AddBasketItem(basket=basket)


class AddReduceFavorites(graphene.Mutation):
    class Arguments:
        obj_id=graphene.Int()
        obj_type=graphene.String()

    favorite_basket=graphene.Field(BasketType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,obj_id,obj_type):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        if not (obj_type in MODELS):
            raise GraphQLError('obj_type motabar nist')

        model = eval(obj_type)
        try:
            product = model.objects.get(pk=obj_id)
        except:
            raise GraphQLError('mahsouli ba in moshakhasat vojd nadarad')

        f_basket, created = Basket.objects.get_or_create(user=info.context.user, status='favorites')
        ct = ContentType.objects.get(model=obj_type.lower())
        try:
            item = f_basket.basketitem_set.get(object_id=obj_id, content_type=ct)
        except:
            item = f_basket.basketitem_set.create(content_type=ct, object_id=obj_id)
            item.count = 1
            item.save()
        else:
            item.count = 0
            item.delete()

        return AddReduceFavorites(favorite_basket=f_basket)




class LikeComment(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        lk=graphene.String()

    comment=graphene.Field(CommentType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,id,lk):
        if not (lk in["1","-1"]):
            raise GraphQLError(" lk must -1 or 1 ")
        try:
            cmnt=Comment.objects.get(pk=id)
        except:
            raise GraphQLError(" in comment vojd nadarad")

        try:
            like = Like.objects.get(user=info.context.user, comment=cmnt)

        except Like.DoesNotExist:
            if lk == "-1":
                Like.objects.create(user=info.context.user, comment=cmnt, dislike=True)
                cmnt.count_dislike += 1
                cmnt.save()

            elif lk == "1":
                Like.objects.create(user=info.context.user, comment=cmnt, like=True)
                cmnt.count_like += 1
                cmnt.save()

        else:
            if lk == "-1":
                if like.dislike == True:
                    cmnt.count_dislike -= 1
                    cmnt.save()
                    like.delete()


                else:
                    like.dislike = True
                    like.like = False
                    like.save()
                    cmnt.count_like -= 1
                    cmnt.count_dislike += 1
                    cmnt.save()


            elif lk == "1":
                if like.like == True:
                    cmnt.count_like -= 1
                    cmnt.save()
                    like.delete()

                else:
                    like.like = True
                    like.dislike = False
                    like.save()
                    cmnt.count_dislike -= 1
                    cmnt.count_like += 1
                    # cmnt.most_liked = cmnt.count_like - cmnt.count_dislike
                    cmnt.save()

        return LikeComment(comment=cmnt)


# class EditeProfile(graphene.Mutation):
#     class Arguments:
#         pass
#
#     profile=graphene.Field(ProfileType)
#
#     @permissions_checker([IsAuthenticated])
#     def mutate(self,info,):
#         pass


class EditAddress(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        lat = graphene.Float()
        lng = graphene.Float()
        province = graphene.String()
        city = graphene.String()
        mailing_address = graphene.String()
        number = graphene.Int()
        mailing_code = graphene.String()
        reciver = graphene.Boolean()
        reciver_first_name = graphene.String()
        reciver_last_name = graphene.String()
        reciver_cellphone = graphene.String()
        reciver_national_code = graphene.String()
        unit = graphene.Int()


    address=graphene.Field(AddressType)
    message=graphene.Field(ResponseType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,id,lat,lng,province,city,mailing_address,number,mailing_code,reciver,reciver_first_name,
               reciver_last_name,reciver_cellphone,reciver_national_code,unit=None):

        try:
           address=Address.objects.get(pk=id,profile=info.context.user.profile)
        except:
            response_error = ResponseType(response_message=" code vared shode motabar nist")
            return EditAddress(message=response_error)
            # return ResponseType(response_message="smmssms")
            # raise GraphQLError('in address vojd nadarad ya motealegh be shoma nist')

        else:
            address.lat=lat
            address.lng=lng
            address.province=province
            address.city=city
            address.mailing_address=mailing_address
            address.number=number
            address.mailing_code=mailing_code
            address.reciver=reciver
            address.reciver_first_name=reciver_first_name
            address.reciver_last=reciver_last_name
            address.reciver_cellphone=reciver_cellphone
            address.reciver_national_code=reciver_national_code
            address.unit=unit if unit is not None else address.unit ############ vali dorost nist bayad None  beshe (baray yadgiri neveshtam)
            address.save()

        return EditAddress(address=address)



class ReduceBasket(graphene.Mutation):
    class Arguments:
        obj_id=graphene.Int()
        obj_type=graphene.String()

    basket=graphene.Field(BasketType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,obj_id,obj_type):

        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        if not(obj_type in MODELS):
            raise GraphQLError('obj_type motabar nist')

        model=eval(obj_type)
        try:
            product=model.objects.get(pk=obj_id)
        except:
            raise GraphQLError('mahsouli ba in moshakhasat vojd nadarad')

        try:
            basket = Basket.objects.get(user=info.context.user, status='active')
        except:
            raise  GraphQLError( "YOU DONT HAVE ANY ACTIVE BASKET")


        try:
            ct = ContentType.objects.get(model=obj_type.lower())
            item = basket.basketitem_set.get(content_type=ct, object_id=obj_id)

            per_price = item.price / item.count
            discount = item.discount / item.count
            item.count -= 1
            item.price -= per_price
            item.discount -= discount
            basket.total_price -= per_price
            basket.total_discount -= discount
            basket.total_discount_price = basket.total_price - basket.total_discount
            basket.save()
            item.save()

            if item.count <= 0:
                item.delete()
                # if basket.basketitem_set.count() <= 0:
                #     basket.delete()


        except:
            raise GraphQLError("YOU DONT HAVE THIS ITEM IN YOUR BASKET")

        else:
            return ReduceBasket(basket=basket)



class AddComment(graphene.Mutation):
    class Arguments:
        obj_id=graphene.Int()
        obj_type=graphene.String()
        viewpoint=graphene.String()
        offer=graphene.String()
        star=graphene.String(default_value='3')
        title=graphene.String()
        good_points=graphene.List(graphene.String)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ['aaa','sss']
        bad_points=graphene.List(graphene.String)

    comment=graphene.Field(CommentType)


    @permissions_checker([IsAuthenticated])
    def mutate(self,info,obj_id,obj_type,viewpoint,good_points=None,bad_points=None,offer=None,star=None,title=None):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        if not (obj_type in MODELS):
            raise GraphQLError('obj_type motabar nist')

        model = eval(obj_type)
        try:
            product = model.objects.get(pk=obj_id)
        except:
            raise GraphQLError('mahsouli ba in moshakhasat vojd nadarad ke shoma beikhay comment bezari')

        ct = ContentType.objects.get(model=obj_type.lower())
        basket_item = BasketItem.objects.filter(content_type=ct, object_id=int(obj_id),
                                                basket__user=info.context.user, basket__delivered=True)

        if bool(basket_item) == True:
            buyer = True
        else:
            buyer = False

        comment=Comment.objects.create(user=info.context.user,content_type=ct,object_id=obj_id,buyer=buyer,
                                       write_date=datetime.date.today(),viewpoint=viewpoint,offer=offer,
                                       star=star,title=title)

        if bool(good_points):
            for opinion in good_points:
                GoodBadPoint.objects.create(comment=comment,point='good',item=opinion)

        if bool(bad_points):
            for opinion in bad_points:
                GoodBadPoint.objects.create(comment=comment,point='bad',item=opinion)

        return AddComment(comment=comment)



class EditComment(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        viewpoint = graphene.String()
        offer = graphene.String()
        star = graphene.String()
        title = graphene.String()
        good_points = graphene.List(graphene.String)
        bad_points = graphene.List(graphene.String)

    comment=graphene.Field(CommentType)
    response=graphene.Field(ResponseType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,id,viewpoint,good_points=None,bad_points=None,star=None,offer=None,title=None):
        # import ipdb; ipdb.set_trace()
        try:
            comment=Comment.objects.get(pk=id,user=info.context.user)
        except:
            raise  GraphQLError('in comment vojd nadarad ya motealegh be shoma nist')

        ct = comment.content_type
        obj_id = comment.object_id
        basket_item = BasketItem.objects.filter(content_type=ct, object_id=int(obj_id),
                                                basket__user=info.context.user, basket__delivered=True)

        if bool(basket_item) == True:
            buyer = True
        else:
            buyer = False


        comment.viewpoint=viewpoint
        # comment.offer=offer if offer is not None else comment.offer #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        comment.offer = offer
        comment.star=star
        comment.title=title
        comment.buyer=buyer
        comment.write_date=datetime.date.today()
        comment.save()

        comment.goodbadpoint_set.all().delete()
        if bool(good_points):
            for opinion in good_points:
                GoodBadPoint.objects.create(comment=comment, point='good', item=opinion)

        if bool(bad_points):
            for opinion in bad_points:
                GoodBadPoint.objects.create(comment=comment, point='bad', item=opinion)

        return EditComment(comment=comment)


class AddDeliveryAddress(graphene.Mutation):
    class Arguments:
        address_id=graphene.Int()
        basket_id=graphene.Int()
        order=graphene.String()

    address=graphene.Field(AddressType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,address_id,basket_id,order,):
        if not(order in ['buy','returned']):
            raise GraphQLError("order must be in ['buy','returned']")

        try:
            address=Address.objects.get(pk=address_id,profile__user=info.context.user)
        except:
            raise GraphQLError("IN ADDRESS VOJOD NADARAD YA MOTEALEGH BE SHOMA NIST ")


        if order == 'buy':
            basket = Basket.objects.get(user=info.context.user, pk=basket_id)
            basket.address = address
            basket.save()


        elif order == 'returned':

            return_basket = ReturningBasket.objects.get(pk=basket_id, user=info.context.user)
            return_basket.address = address
            return_basket.save()

        return AddDeliveryAddress(address=address)



class AddDeliveryDate(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        date_jalali=graphene.String()
        time_range=graphene.String()

    delivery_datetime=graphene.Field(DeliveryDateType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,id,date_jalali,time_range):
        if  not(time_range in ['A','B','C','D']):
            raise GraphQLError("time_range is in ['A','B','C','D']")

        basket = Basket.objects.get(user=info.context.user, pk=id)

        jdate = date_jalali.split("-")
        date = jdatetime.date(year=int(jdate[0]), month=int(jdate[1]), day=int(jdate[2])).togregorian()

        date_range = [datetime.date.today() + datetime.timedelta(i) for i in range(1, 6)]

        if date in date_range:
            time, created = DeliveryDate.objects.get_or_create(date=date, time_range=time_range)
        else:
            raise GraphQLError('date bayat beyn emroz ta 5 roze ayande bashad ') ######## in vaghean nabayad raise bashe


        if not(time.available):
            raise GraphQLError("IN BAZE ZAMANI POR SHODE ")

        if bool(basket.deliverydate) == True:
            previous_delivery_date = basket.deliverydate
            previous_delivery_date.capacity -= 1
            previous_delivery_date.save()
            basket.deliverydate = None
            basket.save()

        # import ipdb; ipdb.set_trace()

        time, created = DeliveryDate.objects.get_or_create(date=date, time_range=time_range)
        basket.deliverydate=time
        basket.save()
        # import ipdb; ipdb.set_trace()
        time.capacity+=1
        time.save()

        return AddDeliveryDate(delivery_datetime=time)

class AAtype(graphene.InputObjectType):
    name=graphene.String()
    age=graphene.Int()


class CancelItemOrBasket(graphene.Mutation):
    class Arguments:
        basket_id=graphene.Int()
        all_items=graphene.Boolean()
        reason=graphene.String()
        obj_list=graphene.List(AAtype)
        # obj_list=graphene.List(graphene.Field,basket_id=graphene.Int(),count=graphene.Int(),reason=graphene.String())#$$$$$$$$$$ [[basket_id, cunt, reason],[basket_id, cunt, reason]]
        #[[

    basket=graphene.Field(BasketType)
    message=graphene.Field(ResponseType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,basket_id,all_items,reason=None,obj_list=None):
        try:
            basket = Basket.objects.get(pk=basket_id, user=info.context.user)
        except:
            # import  ipdb; ipdb.set_trace()
            error_message=ResponseType(response_message="IN basket vojod nadarad ua motealegh be shoma nist")
            return CancelItemOrBasket(message=error_message)
            # raise GraphQLError("IN basket vojod nadarad ua motealegh be shoma nist")
        basket_items = basket.basketitem_set.all()

        import ipdb; ipdb.set_trace()
        if bool(all_items):
            refund_amount = 0
            for basket_item in basket_items:
                refund_amount += (basket_item.price - basket_item.discount)
                basket_item.content_object.stock += basket_item.count
                basket_item.content_object.save()

                cancel_cause, created = CauseOfCancalation.objects.get_or_create(content_type=basket_item.content_type,
                                                                                 object_id=basket_item.object_id,
                                                                                 reason=reason)  # @@@@@@@@@@@@
                cancel_cause.count += 1
                cancel_cause.save()

                basket.status = 'canceled'
                basket.save()


            RefundAmount.objects.create(basket=basket, status='C', amount=refund_amount)
            if basket.deliverydate:
                basket.deliverydate.capacity -= 1
                basket.deliverydate.save()

            return CancelItemOrBasket(basket=basket)



        elif not(bool(all_items)) and bool(obj_list):


            for item in obj_list:
                try:
                    id = item[0]
                    count = item[1]
                    reason = item[2]
                except:
                    raise GraphQLError( 'id ,count,reason vared shavad baray har item')

                try:
                    basket_item = BasketItem.objects.get(pk=basket_id)  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                except:
                    raise  GraphQLError('chenin basket_itemi vojod nadarad')

                if not (basket_item in basket_items):
                    raise GraphQLError('in basket_item  dar in sabad kharid shoma nist')

                if count > basket_item.count:
                    raise GraphQLError( "COUNT bishtar az tedad dar basket shoma")


            refund_amount = 0
            for item in obj_list:
                id = item[0]
                count = item[1]
                reason = item[2]
                basket_item = BasketItem.objects.get(pk=id)
                refund_amount += ((basket_item.price - basket_item.discount) / basket_item.count) * count

                cancel_cause, created = CauseOfCancalation.objects.get_or_create \
                    (content_type=basket_item.content_type, object_id=basket_item.object_id, reason=reason)
                cancel_cause.count += 1
                cancel_cause.save()

                basket_item.content_object.stock += count
                basket_item.content_object.save()

                price = count * (basket_item.price / basket_item.count)
                basket_item.price -= price
                basket.total_price -= price
                discount = count * (basket_item.discount / basket_item.count)
                basket_item.discount -= discount
                basket.total_discount -= discount
                basket_item.count -= count
                basket.total_discount_price = basket.total_price - basket.total_discount
                # basket_item.discount_price =basket_item.price -  basket_item.discount
                basket_item.save()
                basket.save()
                if basket_item.count == 0:
                    basket_item.delete()

            RefundAmount.objects.create(basket=basket, status='C', amount=refund_amount)
            if basket.basketitem_set.count() == 0:
                # basket.delete()#نمیشه چون وقتی این از بین بره تمام وابسته هاش مثل هزینه مرجوعی هم  از بین میره
                basket.status = "canceled"
                basket.save()
            return CauseOfCancalationType(basket=basket)



class LoginRegister(graphene.Mutation):
    class Arguments:
      mobile=graphene.String()

    message = graphene.Field(ResponseType)
    # error=graphene.Field(ErrorType)

    def mutate(self,info,mobile,**kwargs):
        if info.context.user:

            error_message=ResponseType(response_message="bayad login nabashid")
            return LoginRegister(message=error_message)

        rand = str(random.randrange(1000, 10000))
        message = f' کد اعتباری سنجی شما : {rand}'
        user, create = User.objects.get_or_create(username=mobile)
        user_validation, create = ValidationCode.objects.get_or_create(user=user)
        user_validation.validation_code = rand
        user_validation.save()
        main_api = 'https://raygansms.com/SendMessageWithUrl.ashx?'
        url = main_api + urllib.parse.urlencode({'Username': '09123669277', 'Password': '5989231',
                                                 'PhoneNumber': '50002910001080', 'MessageBody': message,
                                                 'RecNumber': mobile, 'Smsclass': '1'})

        json_data = requests.get(url).json()
        response=ResponseType(response_message="کد اعتبارسنجی برای شما ارسال شد.ان را وارد کنید")
        # return LoginRegister(AllMessage)  ########################## mohem
        return LoginRegister(message=response)




class ConfirmCode(graphene.Mutation):
    class Arguments:
        mobile=graphene.String()
        code=graphene.String()

    message=graphene.Field(ResponseType)

    def mutate(self,info,mobile,code,**kwargs):
        try:
            user_code = ValidationCode.objects.get(user__username=mobile).validation_code
            user = User.objects.get(username=mobile)
        except:
            response_error = ResponseType(response_message=" useri ba in moshakhasat vojd nadarad---ya--validation vojd nadarad")
            return ConfirmCode(message=response_error)

        if user_code == code:
            token = get_token(user)
            response_token=ResponseType(response_message=token)
            return ConfirmCode(message=response_token)

        else:
            response_error=ResponseType(response_message=" code vared shode motabar nist")
            return ConfirmCode(message=response_error)




class SendRequestBank(graphene.Mutation):
    class Arguments:
        mobile=graphene.String()
        email=graphene.String()
        description=graphene.String()

    message=graphene.Field(ResponseType)

    @permissions_checker([IsAuthenticated])
    def mutate(self,info,mobile=None,email=None,description=None,**kwargs):
        basket = Basket.objects.get(user=info.context.user, status='active')
        # مربوط به درگاه پرداخت ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
        email = email if email is not None else 'example.com'
        description = description if description is not None else 'توضیحات مربوط به تراکنش را در این قسمت وارد کنید'
        mobile = int(mobile) if mobile is not None else int(basket.user.username)
        CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/'
        amount = int(basket.payable_amount)
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if result.Status == 100:
            # تغیرات بسکت ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            basket.status = 'pardakht'
            basket.order_registration_date = datetime.date.today()
            basket.save()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            message=ResponseType(response_message=("https://sandbox.zarinpal.com/pg/StartPay/" + str(result.Authority)))
            return SendRequestBank(message=message)

        else:
            error_message=ResponseType(response_message='Error code: ' + str(result.Status))
            return SendRequestBank(message=error_message)

        #     return HttpResponse(redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority)).url)
        # else:
        #     return HttpResponse('Error code: ' + str(result.Status))


class Verify(graphene.Mutation):
    class Arguments:
        Status=graphene.String()
        Authority=graphene.String()

    message=graphene.Field(ResponseType)

    def mutate(self,info,Status,Authority,**kwargs):
        basket = Basket.objects.get(user=info.context.user, status='pardakht')
        mobile = basket.user.username
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
        MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        amount = basket.payable_amount
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms
        main_api = 'https://raygansms.com/SendMessageWithUrl.ashx?'
        mobile = basket.user.username
        mobile = '09123669277'

        if Status == 'OK':
            result = client.service.PaymentVerification(MERCHANT, Authority, amount)
            if result.Status == 100:
                basket.status = 'pardakht-shod'
                basket.position = '1'
                basket.save()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms

                url = main_api + urllib.parse.urlencode(
                    {'Username': '09123669277', 'Password': '5989231', 'PhoneNumber': '50002910001080',
                     'MessageBody': f'پرداخت شما موفقیت امیز بود کد بسکت شم{basket.id}', 'RecNumber': mobile,
                     'Smsclass': '1'})
                requests.get(url).json()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
                message=ResponseType(response_message='Transaction success.\nRefID: ' + str(result.RefID))
                return Verify(message=message)
            elif result.Status == 101:
                message = ResponseType(response_message='Transaction submitted : ' + str(result.Status))
                return Verify(message=message)
                # return HttpResponse('Transaction submitted : ' + str(result.Status))


            else:
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms
                url = main_api + urllib.parse.urlencode(
                    {'Username': '09123669277', 'Password': '5989231', 'PhoneNumber': '50002910001080',
                     'MessageBody': f' پرداخت شما موفقیت امیز نبود{result.Status}', 'RecNumber': mobile,
                     'Smsclass': '1'})
                requests.get(url).json()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                message = ResponseType(response_message='Transaction failed.\nStatus: ' + str(result.Status))
                return Verify(message=message)
                # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))

        else:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms
            url = main_api + urllib.parse.urlencode(
                {'Username': '09123669277', 'Password': '5989231', 'PhoneNumber': '50002910001080',
                 'MessageBody': ' پرداخت شما موفقیت امیز نبود', 'RecNumber': mobile,
                 'Smsclass': '1'})
            requests.get(url).json()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            message = ResponseType(response_message='Transaction failed or canceled by user')
            return Verify(message=message)
            # return HttpResponse('Transaction failed or canceled by user')


class AA(graphene.Mutation):
    class Arguments:
        name=graphene.Int(default_value=None)

    message=graphene.Field(ResponseType)

    def mutate(self,info,name,**kwargs):
        ms=ResponseType(response_message=name)
        return AA(message=ms)


############################################# MUTATION ##################################################




class Mutation(graphene.ObjectType):
    # create_address = CreateAddress.Field()
    delete_address=DeleteAddress.Field()
    delete_comment=DeleteComment.Field()

    add_address=AddAddress.Field()
    add_basket_item=AddBasketItem.Field()
    add_reduce_favorites=AddReduceFavorites.Field()
    like_comment=LikeComment.Field()
    # edit_profile=EditeProfile.Field()
    edit_address=EditAddress.Field()
    reduce_basket=ReduceBasket.Field()
    add_comment=AddComment.Field()
    edit_comment=EditComment.Field()
    add_delivery_address=AddDeliveryAddress.Field()
    add_delivery_date=AddDeliveryDate.Field()
    cancel_item_or_basket=CancelItemOrBasket.Field()
    login_register=LoginRegister.Field()
    confirm_code=ConfirmCode.Field()
    send_request_bank=SendRequestBank.Field()
    verify=Verify.Field()


    aa=AA.Field()






# https://stackoverflow.com/questions/49268812/how-to-combine-mutations-to-create-or-login-user-in-django-graphql-jwt
