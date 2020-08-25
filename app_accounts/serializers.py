from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BasketItem, Basket, Profile, Address, Comment, GoodBadPoint, Question, Reply, DeliveryDate, \
    ReturningItem, ReturningDate, ReturningBasket, RefundAmount
from app_product.models import Photo
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import datetime
# from django.core.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

class UserSerializers(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    # username=serializers.CharField(max_length=11)# براش هیچ متدی ننوشتم مشکلی هم نداشت
    """
     token = serializers.SerializerMethodField()# ????????????????????????????????????????????
     def get_token(self, obj, *args, **kwargs):
        token, create = Token.objects.get_or_create(user=obj)
        return token.key
    """

    def validate(self, value):#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        username = value['username']#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        if len(username) == 11 and username.isdigit() and username.startswith('09'):
            return value
        else:
            raise serializers.ValidationError("unvalid  content error-->must be 11 digit character") #@@@@@@@@@@@@@@@@@@@@@


    def create(self, validated_data):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        user = super().create(validated_data)#@@@@@@@@@@@@@@@@@@@@@@@
        user.set_password(validated_data['password'])#@@@@@@@@@@@@@@@@@@@@@@@
        user.save()
        return user #@@@@@@@@@@@@@@@@@@@@@@@

    """
          def update(self,instance,validated_data):
          old_username=instance.username
          old_password=instance.password
          obj=super().update(instance,alidated_data)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
          obj.set_username=old_username
          obj.set_password=old_password
          obj.save()
          return obj
    """

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'required': True}, 'username': {'required': True}}







"""
class Model_Json_Serializers(serializers.Serializer):
     id=serializers.IntegerField(required=True)
     number=serializers.IntegerField(required=True)  
"""
class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs={'first_name':{'required':True},'last_name':{'required':True}}


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    # user = serializers.SerializerMethodField()
    birth_date_jalali=serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.first_name+' '+ obj.user.last_name #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def get_email(self, obj):
        return obj.user.email

    # def get_user(self, obj): # این هم خروجی درست میده
    #     return obj.user.username
    def get_birth_date_jalali(self,obj):
        return obj.birth_date_jalali

    class Meta:
        model = Profile
        #fields='__all__' # با این هم مشکلی نداشت
        exclude = ['id']



class EditProfileSerializer(serializers.ModelSerializer):
    # first_name=serializers.CharField(max_length=30)
    # last_name=serializers.CharField(max_length=30)
    # email=serializers.EmailField(required=False)
    birth_date_jalali=serializers.CharField()


    class Meta:
        model = Profile
        fields = ('birth_date_jalali','national_code','bank_card','newsletter_receive',
                  'foreign_national')
        #fields='__all__' # روی این کار نمیکنه
        # exclude=['user']
        extra_kwargs={'birth_date_jalali':{'required':True},'foreign_national':{'required':True},
                      'newsletter_receive':{'required':True}}



class FavoritesItemSerializer(serializers.ModelSerializer):
    price=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    image_url=serializers.SerializerMethodField()
    product_id=serializers.SerializerMethodField()
    product_model=serializers.SerializerMethodField()

    def get_price(self,obj):
        return  obj.content_object.price

    def get_name(self,obj):
        return obj.content_object.name

    def get_image_url(self,obj):

        if obj.content_object.photo.first():#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            return obj.content_object.photo.first().image_url  #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        else:
            return None#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    def get_product_id(self,obj):
        return obj.object_id

    def get_product_model(self,obj):
        return str(obj.content_type)


    class Meta:
        model=BasketItem
        fields=('price','name','image_url','product_model','product_id')


class BasketItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    price_one_item = serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    model=serializers.SerializerMethodField()
    product_id=serializers.SerializerMethodField()
    product_model=serializers.SerializerMethodField()

    def get_image(self,obj):
        product_item=obj.content_object
        image=Photo.objects.filter(content_type=obj.content_type,object_id=obj.object_id).first()#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if image:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            return image.image_url
        else:
            return None


    def get_item(self, obj, *args, **kwargs):
        return obj.content_object.name  #@@@@@@@@@@@@@@@@@@@@@@@

    def get_price_one_item(self, obj, *args, **kwargs):
        return (obj.price -obj.discount) /obj.count #@@@@@@@@@@@@@@@@@@@@@@@

    def get_model(self,obj):
        return str(ContentType.objects.get_for_model(obj))
    def get_product_id(self,obj):
        return obj.object_id

    def get_product_model(self,obj):
        return str(obj.content_type)

    class Meta:
        model = BasketItem
        fields = ['item','image','count','content_type', 'price_one_item','price','discount',
                  'discount_price','id','model','product_id','product_model']
        #depth = 1


class BasketSerializer(serializers.ModelSerializer):
    commodity_count=serializers.SerializerMethodField()#فقط خواندنی است
    item_list = serializers.SerializerMethodField()
    total_discount_persent=serializers.SerializerMethodField()

    def get_commodity_count(self,obj):
        basket_items=obj.basketitem_set.all()
        count=0
        for item in basket_items:
            count+=item.count
        return count

    def get_item_list(self,obj): #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        items = obj.basketitem_set.all()
        request = self.context['request']

        paginator=PageNumberPagination()
        pagination_basketitem=paginator.paginate_queryset(items,request)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        ser = BasketItemSerializer(pagination_basketitem, many=True)
        return ser.data #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def get_total_discount_persent(self,obj):
        return obj.total_discount/obj.total_price


    class Meta:
        model = Basket
        # fields = '__all__'
        fields = ('commodity_count','total_price','total_discount','total_discount_persent',
                  'total_discount_price','shipping_cost','payable_amount','item_list')

#
# class BasketFavoriteSerializer(serializers.ModelSerializer):
#     item = serializers.SerializerMethodField()  # فقط خواندنی است
#     price = serializers.SerializerMethodField()
#
#     def get_item(self, obj, *args, **kwargs):
#         return obj.content_object.name
#
#     def get_price(self, obj, *args, **kwargs):
#         return obj.content_object.price
#
#
#     class Meta:
#         model=BasketItem
#         fields=('price','item')



class AddressSerializer(serializers.ModelSerializer):
    reciver_full_name=serializers.SerializerMethodField()
    def get_reciver_full_name(self,obj):
        # if obj.reciver==True:
        #   return obj.profile.user.first_name+" "+obj.profile.user.last_name #@@@@@@@@@@@@@@@@@@@@@@@@@@
        return obj.reciver_first_name + "  " + obj.reciver_last_name

    # def get_profile(self,obj):
    #     #profile=obj.objects.get(profile__user==request.user)
    #     #Profile.objects.get()
    #     #return obj.profile.user.id
    #     return obj.profile_id #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    class Meta:
        model=Address
        # fields='__all__'
        # #exclude = ['profile']
        fields=('province','city','mailing_address','mailing_code','reciver_full_name','reciver_cellphone')



class AddAddressSerializer(serializers.ModelSerializer):
     class Meta:
         model=Address

         exclude=['profile','id']
         extra_kwargs = {'lat': { 'required': True},'lng': { 'required': True},
                         'province':{ 'required': True},'city':{ 'required': True},
                         'mailing_address':{ 'required': True},'number':{ 'required': True},
                         'mailing_code': {'required': True},'reciver':{ 'required': True},
                         'reciver_first_name':{ 'required': True},'reciver_last_name':{ 'required': True},
                         'reciver_national_code':{ 'required': True},
                         'reciver_cellphone': {'required': True}
                         }#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #



#
# class UpdateAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         exclude = ['profile', 'id']
#         extra_kwargs = {'lat': {'required': True}, 'lng': {'required': True},
#                         'reciver': {'required': True},'reciver_first_name': {'required': True},
#                         'reciver_last_name': {'required': True},'reciver_national_code': {'required': True}}







class CommentSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    good_point=serializers.SerializerMethodField()
    bad_point=serializers.SerializerMethodField()
    image_url=serializers.SerializerMethodField()
    product_id=serializers.SerializerMethodField()
    write_date_jalali=serializers.SerializerMethodField()

    # def get_product_item(self,obj):
    #     return obj.content_object.name

    def get_good_point(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        items=obj.goodbadpoint_set.filter(point='good')
        text=''
        for point in items:
            text+=point.item+" , "
        return text

    def get_bad_point(self, obj):
        items = obj.goodbadpoint_set.filter(point='bad')
        text = ''
        for point in items:
            text += point.item + ", "
        return text


    def get_user(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        user= obj.user.first_name
        if bool(user):
            return user
        else:
            return ("digikala user=کاربر دیجیکالا")

    def get_image_url(self,obj):
        image=obj.content_object.photo.first()#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        if image:
            return obj.content_object.photo.first().image_url#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        else:
            return None
    def get_product_id(self,obj):
        return obj.object_id

    def get_product_model(self,obj):
        return str(obj.content_type)

    def get_write_date_jalali(self,obj):
        return obj.write_date_jalali

    class Meta:
        model=Comment
        # fields=('title','viewpoint','strengths','weak_points','user','write_date','buyer')
        exclude = ['id','content_type','object_id']



class CommentSerializer1(serializers.Serializer):#خیلی خیلی مهههم کلش @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    product_item=serializers.SerializerMethodField()
    avg_star=serializers.SerializerMethodField()
    number_of_voter=serializers.SerializerMethodField()
    comments=serializers.SerializerMethodField()

    def get_avg_star(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        comments=obj.comments.all() #@@@@@@@@@@@@@@@@@@
        count=comments.count()
        if count>0 :
            sum = 0
            for cm in comments:
                sum += int(cm.star)  # @@@@@@@@@@@@@@@@@@@@@
            return sum/count
        else:
            return 0

    def get_number_of_voter(self,obj):
        count=obj.comments.all().count()
        return count


    def get_product_item(self,obj):
        return obj.name

    def get_comments(self,obj):
        comments=self.context['comments'] #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        request=self.context['request']

        paginator = PageNumberPagination()#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        paginator.page_size = 3#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        pagination_comments = paginator.paginate_queryset(comments,request)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        ser=CommentSerializer(pagination_comments,many=True)
        return ser.data





class GoodBadPointSerializer(serializers.ModelSerializer):
    item=serializers.CharField(max_length=2000,required=True)
    point= serializers.CharField(max_length=2000, required=True)

    # def create(self,validated_data):
    #     # import ipdb; ipdb.set_trace()
    #     obj=super().create(validated_data)
    class Meta:
        model=GoodBadPoint
        fields=['point','item']
        # extra_kwargs={'item':{'rquired':True},'point':{'rquired':True}}


class AddComment2Serializer(serializers.ModelSerializer):
    good_bad_points=GoodBadPointSerializer(many=True,required=False) #خیییلیی مهم @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def validate_offer(self,value):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # import ipdb; ipdb.set_trace()
        buyer=self.context['buyer']
        if buyer==True:
            return value #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        else:
            return None


    def create(self,validated_data): #مههههههههههههم کلش $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        try:
            points=validated_data.pop('good_bad_points') #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            ser=GoodBadPointSerializer(data=points,many=True)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

            if ser.is_valid():
                comment = Comment.objects.create(**validated_data, write_date=datetime.date.today())  # @@@@@@@@@@@@@@@@
                ser.save(comment=comment) #به ازای هرکد. یک comment==comment@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                return comment #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            else:
                 return ser.errors #@@@@@@@@@@@@@@@@@@@@@@@@@@@

        except:
            comment = Comment.objects.create(**validated_data, write_date=datetime.date.today())#@@@@@@@@@@@@@@@@@
            return comment


    def update(self,obj, validated_data):
        try:

            points = validated_data.pop('good_bad_points')#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            good_bad_points=GoodBadPoint.objects.filter(comment=obj)
            for i in good_bad_points:
                i.delete()


            # if bool(points):
            #     for i in points:
            #         # import ipdb; ipdb.set_trace()
            #         if (i.get('point') in ['bad','good']) and i.get('item'):
            #             pass
            #
            #         else:
            #             raise serializers.ValidationError(" point or item dorost vared nashode")
            #
            #     for i in points:
            #            GoodBadPoint.objects.create(point=i.get('point'),item=i.get('item'))
            #     return instance
            #
            #
            # else:
            #     return instance


            ser = GoodBadPointSerializer(data=points, many=True)
            if ser.is_valid():
                ser.save(comment=obj)
                obj.viewpoint = validated_data.get('viewpoint', obj.viewpoint)
                obj.star = validated_data.get('star', obj.star)
                obj.title = validated_data.get('title', obj.title)
                obj.offer = validated_data.get('offer', obj.offer)
                obj.save()

                return obj
            else:
                return ser.errors

        except:
            good_bad_points = GoodBadPoint.objects.filter(comment=obj)
            for i in good_bad_points:
                i.delete()
            # obj.viewpoint = validated_data.get('viewpoint', obj.viewpoint)
            obj.viewpoint = validated_data.get('viewpoint')
            obj.star = validated_data.get('star',"3")
            obj.title = validated_data.get('title')
            obj.offer = validated_data.get('offer')
            obj.save()

            return obj
            # comment = Comment.objects.create(**validated_data, write_date=datetime.date.today())



    class Meta:
        model = Comment
        fields = ('title', 'viewpoint','star','offer','good_bad_points')
        extra_kwargs={'viewpoint':{'required':True}}



class OrderSerializer(serializers.ModelSerializer):
    image_items=serializers.SerializerMethodField()
    order_registration_date_jalali=serializers.SerializerMethodField()

    def get_order_registration_date_jalali(self,obj):
        return obj.order_registration_date_jalali

    def get_image_items(self,obj):
        items=obj.basketitem_set.all()
        ser=BasketItemSerializer(items,many=True)
        return ser.data

    class Meta:
        model=Basket
        # exclude=['user','delivery_date','address','id']
        fields=['order_number','order_registration_date','order_registration_date_jalali','status','payable_amount','position','image_items']



# class OrderItemSerializer(serializers.ModelSerializer):
#     items = serializers.SerializerMethodField()
#     reciver_first_name=serializers.SerializerMethodField()
#     reciver_last_name=serializers.SerializerMethodField()
#     reciver_mailing_address=serializers.SerializerMethodField()
#     province=serializers.SerializerMethodField()
#     city=serializers.SerializerMethodField()
#     number=serializers.SerializerMethodField()
#     reciver_cellphone=serializers.SerializerMethodField()
#     payable_amount=serializers.SerializerMethodField()
#     shipping_cost = serializers.SerializerMethodField()
#     deliverydate=serializers.SerializerMethodField()
#     deliverytime = serializers.SerializerMethodField()
#
#
#     def get_items(self, obj):
#         items = obj.basketitem_set.all()
#         ser = BasketItemSerializer(items, many=True)
#         return ser.data
#
#     def get_reciver_last_name(self, obj):
#         return obj.address.reciver_last_name
#
#     def get_reciver_first_name(self, obj):
#         return obj.address.reciver_first_name
#
#     def get_reciver_mailing_address(self,obj):
#        return obj.address.mailing_address
#
#     def get_province(self,obj):
#         return obj.address.province
#
#     def get_city(self,obj):
#         return obj.address.city
#     def get_number(self,obj):
#         return obj.address.number
#
#     def get_reciver_cellphone(self, obj):
#         return obj.address.reciver_cellphone
#
#     def get_payable_amount(self,obj):
#         return obj.payable_amount
#
#     def get_shipping_cost(self, obj):
#         return obj.shipping_cost
#
#     def get_deliverydate(self,obj):
#         return obj.deliverydate.date
#
#     def get_deliverytime(self,obj):
#         return obj.deliverydate.time_range
#
#     class Meta:
#         model=Basket
#         exclude=['id','user','address',]
#
#
# class QuestionSerializer(serializers.ModelSerializer):
#
#     def create(self,validated_data):
#         obj=super().create(validated_data)
#         # import ipdb; ipdb.set_trace()
#         obj.posted_date=datetime.date.today()#@@@@@@@@@@@@@@@@@@@@
#         obj.save()
#         return obj
#
#     class Meta:
#         model=Question
#         fields=('text','posted_date')
#         # extra_kwargs={'text':{'rquired':True}}


class OrderItemSerializer(serializers.ModelSerializer):
    address_info=serializers.SerializerMethodField()
    items_info=serializers.SerializerMethodField()
    delivery_date_time=serializers.SerializerMethodField()
    refund_amount=serializers.SerializerMethodField()
    order_registration_date_jalali=serializers.SerializerMethodField()

    def get_address_info(self,obj):
        ser=AddAddressSerializer(obj.address)
        return ser.data

    def get_items_info(self,obj):
        items=obj.basketitem_set.all()
        ser=BasketItemSerializer(items,many=True)
        return ser.data

    def get_delivery_date_time(self,obj):
        if obj.deliverydate:
            ser=DeliveryDateSerializer(obj.deliverydate)
            return ser.data
        else:
            return None


    def get_refund_amount(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # import ipdb; ipdb.set_trace()
        all_refund_amount=RefundAmount.objects.filter(basket=obj,status='R')
        sum=0
        for i in all_refund_amount:
            sum+=i.amount
        return sum

    def get_order_registration_date_jalali(self,obj):
        return obj.order_registration_date_jalali

    class Meta:
        model=Basket
        fields=['order_registration_date','order_registration_date_jalali','order_number','total_discount_price','payable_amount',
                'shipping_cost','position','refund_amount','delivery_date_time','address_info',
                'items_info',]































class ReplyQuestionSerializer(serializers.ModelSerializer):

    def create(self,validated_data):
        obj = super().create(validated_data)
        baskets=Basket.objects.filter(user=self.context['request'].user,status='delivered')
        # import ipdb; ipdb.set_trace()
        for basket in baskets:
            items=basket.basketitem_set.filter(content_type=ContentType.objects.get_for_model(self.context['product']),
                                               object_id=self.context['product'].id)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            if bool(items):
                obj.buyer=True
                obj.save()
                break
        return obj



        return obj

    class Meta:
        model=Reply
        fields=('text','buyer')


class ShowQuestionSerializer(serializers.Serializer):
    number_of_questions=serializers.SerializerMethodField()
    def get_number_of_questions(self,obj):
        return len(self.context['questions'])


class DeliveryDateSerializer(serializers.ModelSerializer):#این سریالایزرش سخت بود برام و پر از جدید@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    available=serializers.SerializerMethodField()
    # date=serializers.DateField()
    # def validate_date(self,value):
          # value=datetime.strptime(value, '%Y-%m-%d').date() #@@@@@@@@@@@@@@@@@@@@@@@@@@@ نیازی بهش نبود تو سریالایزر
          # date_range = [datetime.date.today() + datetime.timedelta(i) for i in range(1, 6)]
          #
          # if value in date_range:
          #     return value
          # else:
          #     raise serializers.ValidationError('DATE RANGE IS BETWEN TOMORROW  TA 5 ROZ BAD AZ ON')

    def get_available(self,obj): #داخلش  مقذار یک فیلد دیگه رو هم تغییر دادیم@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if obj.available:
            obj.capacity += 1
            obj.save()
            return True
        else:
            raise serializers.ValidationError("mor than capacity") #@@@@@@@@@@@@@@@@@@@@@@@@@@

    class Meta:
        model=DeliveryDate
        fields=('available','date','range_time','date_jalali')


class ReturningDateSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReturningDate
        fields=('returning_date','returning_date_jalali','range_time')


class ReturningItemSerializer(serializers.ModelSerializer):
    returning_basket_item_name=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()

    def get_returning_basket_item_name(self,obj):
        rb_name=obj.basket_item.content_object.name
        return rb_name

    def get_image(self,obj):
        image=obj.basket_item.content_object.photo.first()
        if image:
            return obj.basket_item.content_object.photo.first().image_url #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        else:
            return None

    class Meta:
        model=ReturningItem
        exclude = ['returning_basket','id','basket_item','descriptions']



class ReturningBasketSerializer(serializers.ModelSerializer):
    address=serializers.SerializerMethodField()
    returning_date=serializers.SerializerMethodField()
    returning_items=serializers.SerializerMethodField()

    def get_address(self,obj):#از نظر منطفی که نوشته شده توجه کن $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        if obj.address:
            ser=AddAddressSerializer(obj.address)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            return ser.data
        else:
            return None

    def get_returning_date(self, obj):
        if bool(obj.returning_date):
            ser = ReturningDateSerializer(obj.returning_date)  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            return ser.data
        else:
            return None

    def get_returning_items(self, obj):
        item = obj.returningitem_set.all()
        ser = ReturningItemSerializer(item, many=True)
        return ser.data

    class Meta:
        model = ReturningBasket
        fields = ['status', 'address', 'returning_date', 'returning_items']


class AddReturnItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@
        obj = super().create(validated_data)
        obj.purchase_amount = ((obj.basket_item.price - obj.basket_item.discount) / obj.basket_item.count) * obj.count  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        obj.save()
        return obj

    def update(self, obj, validated_data):  # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        obj.purchase_amount = (( obj.basket_item.price - obj.basket_item.discount) / obj.basket_item.count) * validated_data.get( 'count')  # $$$$$$$$$$$$$$$$$$$$$$$$$
        obj.count = validated_data.get('count', obj.count)  # $$$$$$$$$$$$$$$$$$$$$$$$$$
        obj.reason = validated_data.get('reason', obj.reason)
        obj.descriptions = validated_data.get('descriptions', obj.descriptions)
        obj.save()  # حتما اخر بازنویسی تمام فیلدها نوشته بشه وگرنه فیلدهای بعدش مقدار جدید رو نمیگیرن و همون مقدار قبلیشون هست
        return obj

    class Meta:
        model = ReturningItem
        exclude = ['returning_basket', 'status', 'basket_item']
        extra_kwargs = {'count': {'required': True}, 'reason': {'required': True}, 'descriptions': {'required': True}}


class ReturnItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product_model = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.basket_item.content_object.photo.first():  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            return obj.basket_item.content_object.photo.first().image_url  # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        else:
            return None

    def get_product_model(self, obj):
        # import ipdb; ipdb.set_trace()
        return str(obj.basket_item.content_type)

    def get_product_id(self, obj):
        return obj.basket_item.object_id

    class Meta:
        model = ReturningItem
        fields = ('image', 'product_model', 'product_id')


class ReturnedBasketSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    order_number = serializers.SerializerMethodField()

    def get_items(self, obj):
        item = obj.returningitem_set.all()
        ser = ReturnItemSerializer(item, many=True)
        return ser.data  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def get_order_number(self, obj):
        return obj.basket.order_number

    class Meta:
        model = ReturningBasket
        fields = ['registration_date', 'status', 'order_number', 'items']
