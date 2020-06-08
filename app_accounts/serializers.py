from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BasketItem, Basket, Profile,Address,Comment,GoodBadPoint
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username=serializers.CharField(max_length=11)# براش هیچ متدی ننوشتم مشکلی هم نداشت
    # first_name = serializers.CharField(max_length=2)اگر چنین چیزی بود اجباری میشد وارد کردنش
    """
     token = serializers.SerializerMethodField()# چرا توکن نوشتیم؟؟؟
     def get_token(self, obj, *args, **kwargs):
        token, create = Token.objects.get_or_create(user=obj)
        return token.key
    """
    class Meta:
         model = User
         fields = ('username', 'first_name', 'last_name', 'email', 'password')
         # fields = '__all__'


    def validate(self, data):##################################
        username = data['username']##################################
        if len(username) == 11 and username.isdigit() and username.startswith('09'):
            return data
        else:
            raise serializers.ValidationError("unvalid  content error-->must be 11 digit character")


    def create(self, validated_data):#??????????????????????
        user = super().create(validated_data)
        # import ipdb; ipdb.set_trace()
        user.set_password(validated_data['password'])
        user.save()
        return user

    """
          def update(self,instance,validated_data):
          old_username=instance.username
          old_password=instance.password
          obj=super().update(instance,alidated_data)
          obj.set_username=old_username
          obj.set_password=old_password
          obj.save()
          return obj 
    """

"""
class Model_Json_Serializers(serializers.Serializer):
     id=serializers.IntegerField(required=True)
     number=serializers.IntegerField(required=True)  
"""
class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    # user = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.first_name+' '+ obj.user.last_name #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def get_email(self, obj):
        return obj.user.email

    # def get_user(self, obj): # این هم خروجی درست میده
    #     return obj.user.username

    class Meta:
        model = Profile
        #fields='__all__' # با این هم مشکلی نداشت
        exclude = ['id']


class EditProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('birth_date','national_code','bank_kard','newsletter_receive','foreign_national')
        #fields='__all__' # روی این کار نمیکنه
        # exclude=['user']



class BasketItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField() #فقط خواندنی است
    price = serializers.SerializerMethodField()

    def get_item(self, obj, *args, **kwargs):
        return obj.content_object.name  #@@@@@@@@@@@@@@@@@@@@@@@

    def get_price(self, obj, *args, **kwargs):
        return obj.content_object.price * obj.count #@@@@@@@@@@@@@@@@@@@@@@@

    class Meta:
        model = BasketItem
        fields = ('count', 'basket', 'content_type', 'price', 'item')
        #depth = 1


class BasketSerializer(serializers.ModelSerializer):
    item_list = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_item_list(self,obj): #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        item = obj.basketitem_set.all()
        ser = BasketItemSerializer(item, many=True)
        return ser.data

    def get_total_price(self,obj, *args, **kwargs):#@@@@@@@@@@@@@@@@@@@@@@@
        items = obj.basketitem_set.all()
        result = 0
        for item in items:
            result += item.content_object.price * item.count#جدید
        return result

    class Meta:
        model = Basket
        # fields = '__all__'
        fields = ('item_list','total_price',)


class BasketFavoriteSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()  # فقط خواندنی است
    price = serializers.SerializerMethodField()

    def get_item(self, obj, *args, **kwargs):
        return obj.content_object.name

    def get_price(self, obj, *args, **kwargs):
        return obj.content_object.price


    class Meta:
        model=BasketItem
        fields=('price','item')



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
                         'reciver_national_code':{ 'required': True}}#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


class UpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['profile', 'id']
        extra_kwargs = {'lat': {'required': True}, 'lng': {'required': True},
                        'reciver': {'required': True},'reciver_first_name': {'required': True}, 'reciver_last_name': {'required': True},
                        'reciver_national_code': {'required': True}}

# class CommentSerializer1(serializers.ModelSerializer):
#
#     comment=serializers.SerializerMethodField()
#     def get_comment(self,obj):
#         import ipdb; ipdb.set_trace()
#         comment=Comment.objects.get()
#     class Meta:
#         model=Comment
#         fields="__all__"



class CommentSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    good_point=serializers.SerializerMethodField()
    bad_point=serializers.SerializerMethodField()

    def get_good_point(self,obj):
        # import ipdb; ipdb.set_trace()
        items=obj.goodbadpoint_set.filter(point='good')
        text=''
        for point in items:
            text+=point.item+","
        return text

    def get_bad_point(self, obj):

        items = obj.goodbadpoint_set.filter(point='bad')#@@@@@@@@@@@@@@@@@
        text = ''
        for point in items:

            text += point.item + ","
        return text
    # def get_like(self,obj):
    #     return obj.like_set.filter(like=True).count()
    #
    # def get_dislike(self,obj):
    #     return obj.like_set.filter(dislike=True).count()

    def get_user(self,obj):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        user= obj.user.first_name
        if bool(user):
            return user
        else:
            return ("digikala user=کاربر دیجیکالا")

    class Meta:
        model=Comment
        # fields=('title','viewpoint','strengths','weak_points','user','write_date','buyer')
        exclude = ['id','content_type','object_id','publish']





class add_comment_serializer(serializers.ModelSerializer):
    average_star=serializers.SerializerMethodField()
    def get_average_star(self,obj):
        pass
    class Meta:
        pass

class AddCommentSerializer(serializers.ModelSerializer):

    user=serializers.SerializerMethodField()
    def get_user(self,obj):

        user = self.context['request'].user
        return user

    class Meta:
        model=Comment
        # fields=('title','viewpoint','strengths','weak_points','user','write_date','buyer')
        fields=('title','viewpoint','strengths','weak_points','user')
#
# class AddComment2Serializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#
#     def get_user(self, obj):
#         print("*"*100)
#     #     import ipdb ; ipdb.set_trace()
#         user = self.context['request'].user
#         return user
#
#     class Meta:
#         model = Comment
#         # fields=('title','viewpoint','strengths','weak_points','user','write_date','buyer')
#         fields = ('title', 'viewpoint', 'strengths', 'weak_points','user')

class GoodBadPointSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        import ipdb; ipdb.set_trace()
        obj=super().create(validated_data)
    class Meta:
        model=GoodBadPoint
        fields=("point","item")


class AddComment2Serializer(serializers.ModelSerializer):
    viewpoint = serializers.CharField(max_length=2000)
    # most_liked=serializers.IntegerField(default=0)



    def create(self, validated_data):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        obj = super().create(validated_data)
        obj.write_date = timezone.now()
        obj.save()

        return obj


    class Meta:
        model = Comment
        # fields=('title','viewpoint','strengths','weak_points','user','write_date','buyer')
        fields = ('title', 'viewpoint','star')
        # fields='__all__'




class OrderSerializer(serializers.ModelSerializer):
    items=serializers.SerializerMethodField()
    def get_items(self,obj):
        items=obj.basketitem_set.all()
        ser=BasketItemSerializer(items,many=True)
        return ser.data
    class Meta:
        model=Basket
        exclude=['user','delivered_date','address','id']


class OrderItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    reciver_first_name=serializers.SerializerMethodField()
    reciver_last_name=serializers.SerializerMethodField()
    reciver_mailing_address=serializers.SerializerMethodField()
    reciver_cellphone=serializers.SerializerMethodField()

    def get_items(self, obj):
        items = obj.basketitem_set.all()
        ser = BasketItemSerializer(items, many=True)
        return ser.data

    def get_reciver_last_name(self, obj):
        return obj.address.reciver_last_name

    def get_reciver_first_name(self, obj):
        return obj.address.reciver_first_name


    def get_reciver_cellphone(self,obj):
        return obj.address.reciver_cellphone

    def get_reciver_mailing_address(self,obj):
       return obj.address.mailing_address


    class Meta:
        model=Basket
        exclude=['id','user','address']
