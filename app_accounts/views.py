from django.shortcuts import render
import random
import datetime
# from datetime import datetime as dt #این برای اون strptime لازم هست @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers, BasketItemSerializer, BasketSerializer, ProfileSerializer,\
    EditProfileSerializer, UserSerializer2,AddressSerializer,AddAddressSerializer,\
    CommentSerializer,AddComment2Serializer,GoodBadPointSerializer,OrderSerializer,OrderItemSerializer,\
    ReplyQuestionSerializer,ShowQuestionSerializer,DeliveryDateSerializer,\
    ReturningBasketSerializer,AddReturnItemSerializer,ReturnedBasketSerializer,CommentSerializer1,\
    FavoritesItemSerializer

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app_accounts.permissions import IsOwner, MustAnonymouse,Comment_Owner,PublishPermission,\
    JustOneComment,IsNotOwner,AdressRegisterAbility,ActiveTrueBasket,ReturnTimeLimit,AllowedToSet,\
    AllowCancelledReturnBasket,CancelledTimeLimit,HaveInactiveReturningBasket,HaveActiveReturningBasket,\
    YourOrder,YourReturnBasket
from .models import BasketItem, Basket, Profile,Address,Comment,Like,Question,Reply,\
    DeliveryDate,ReturningBasket,ReturningDate,ReturningItem,RefundAmount,ValidationCode

from app_product.models import Cellphone, Tablet, Laptop, Television,CauseOfCancalation
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
# from passlib.hash import pbkdf2_sha256
from kavenegar import *
from rest_framework.pagination import PageNumberPagination
import requests
import urllib.parse
from rest_framework.authtoken.models import Token



@api_view(['POST'])
@permission_classes((MustAnonymouse,))
def register(request):
    ser = UserSerializers(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response({'message':'sabt name shoma anjam shod'})
    else:
        return Response(ser.errors)

# @api_view(['POST'])
# @permission_classes((MustAnonymouse,))
# def register(request):
#     ser = UserSerializers(data=request.data)
#     if ser.is_valid():
#             api = KavenegarAPI('306174674767677366326F396C74555032367A31774E68384D784B55674A3163765958463174662B3252383D')
#             params = {'sender': '1000596446',
#                       'receptor': ser.data['username'],
#                       'message': f'کداعتبارسنجی شما {random.randrange(10000,100000)} '}
#             response = api.sms_send(params)
#             return Response({"STATUS": "OK", "MSG": "کد اعتاری به حساب شما ارسال شد"})
#
#
#         ## except APIException as e:
#         ##    print(e)
#         ## except HTTPException as e:
#         ##     print(e)
#
#
#         ## import ipdb; ipdb.set_trace()
#         ## register_data=int(ser.data['username'])
#
#
#     else:
#         return Response(ser.errors)

"""
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ProfileView(request):
   try:
        user = User.objects.get(username=request.user)
   except:
        return Response({"ERROR": "WE DONT HAVE THIS USERNAME"})
   else:
        ser=UserSerializers(user)
        return Response(ser.data)"""
"""

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    try:
        old_password=request.data['old_password']
        new_password=request.data['new_password']
        repeat_new_password=request.data['repeat_new_password']
    except:
        return Response({"ERROR":"ERROR1"})
    #import ipdb; ipdb.set_trace()
    # old_password=set_password()
    # hashed_pwd = make_password(old_password)
    #check_password(password, hashed_pwd)
    #######
    #data = self.cleaned_data['old_password']
    #enc_passsword=pbkdf2_sha256.encrypt(old_password,rounds=12000,salt_size=32)
    ######
    if check_password(old_password,request.user.password) :
        if new_password==repeat_new_password:
            hashed_pwd = make_password(new_password)
            request.user.password=hashed_pwd
            request.user.save()
            return Response({'MESSAGE':"NEW PASSWORD "})
        else:
            return Response({"ERROR":"2 PASSWORD BAYAD SHABIH BASHAD"})
    else:
        return Response({"ERROR":"OLD PASSWORD RA DOROST VARED KONID"})"""


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    try:
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        repeat_new_password = request.data['repeat_new_password']
    except:
        return Response({"error":" 'old_password' ya 'new_password' ya 'repeat_new_password' ra vared nakarid"})

    if check_password(old_password, request.user.password):#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        if new_password == repeat_new_password:
            request.user.password = make_password(new_password)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            request.user.save()
            return Response({'MESSAGE': "NEW PASSWORD CREATED "})
        else:
            return Response({"ERROR": "2 PASSWORD BAYAD SHABIH BASHAD"})
    else:
        return Response({"ERROR": "OLD PASSWORD RA DOROST VARED KONID"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile(request):
    profile=request.user.profile
    ser = ProfileSerializer(profile)
    return Response(ser.data)


@api_view(['PUT'])#@@@@@@@@@@@@@@@@@@@@@@@@@@@@ این به نظرم مثال خوبیست چون از دوتا سریالایزر استفاده کردم
@permission_classes((IsAuthenticated,))
def edit_profile(request):
       profile = Profile.objects.get(user=request.user)
       ser = EditProfileSerializer(profile, data=request.data)
       if ser.is_valid():
           pass
       else:
           return Response(ser.errors)

       user = User.objects.get(username=request.user)
       ser2=UserSerializer2(user, data=request.data)
       if ser2.is_valid():
          pass

       else:
           return Response(ser2.errors)

       ser.save()
       ser2.save()

       ser=ser.data  # فهیمه این خط و چند خط پایین برای این هست که بتونی دو تا دیکشنری رو به هم الحاق کنی > یادت هست update رو؟
       ser2=ser2.data
       ser.update(ser2)#@@@@@@@@@@@@@@@@@@@@@@@@@@@
       return Response(ser)
       #api_root = reverse_lazy('profile', request=request)  <--  برگرداندن یک دیگر URL

"""
@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated, IsOwner))
def EditProfileView(request):
    user = User.objects.get(username=request.query_params['username'])

    if request.method == 'PUT':
        ser = UserSerializers(user, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response({"ERROR": "DATA NOT VALID"})


    elif request.method == 'GET':
        ser = UserSerializers(user)
        return Response(ser.data)
        """


########################################################################
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_address(request):
    profile=Profile.objects.get(user=request.user)
    addresses=profile.address_set.all()
    paginate=PageNumberPagination()#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    paginate.page_size=1#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    pagination_address=paginate.paginate_queryset(addresses,request)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    ser=AddressSerializer(pagination_address,many=True)
    return Response(ser.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_address(request):

    prf=Profile.objects.get(user=request.user)
    ser=AddAddressSerializer(data=request.data)
    if ser.is_valid():

        ser.save(profile=prf)
        return Response(ser.data)
    else:
        return Response(ser.errors)


@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated,IsOwner))
def edit_address(request,pk):
    address = Address.objects.get(pk=pk)
    if request.method=='GET':
        ser=AddAddressSerializer(address)
        return Response(ser.data)

    elif request.method=='PUT':
        # ser=UpdateAddressSerializer(address,data=request.data) #اگر همه یفیلدها اجباری نبودن اینو جایگزین خط پایین کن
        ser=AddAddressSerializer(address,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,IsOwner))
def delete_address(request,pk):
    address=Address.objects.get(pk=pk)
    address.delete()

    addresses=Address.objects.filter(profile__user=request.user)
    ser=AddressSerializer(addresses, many=True)
    return Response(ser.data)



"""
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_basket_item(request):
    basket_item = BasketItem.objects.filter(basket__user=request.user, basket__status='active')
    ser = BasketItemSerializer(basket_item, many=True)
    return Response(ser.data)"""

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_basket_item(request):
    try :
        obj_id=request.data['obj_id']
        obj_type=request.data['obj_type']
    except:
         return Response({"ERROR:": "ID OR MODEL DOES NOT EXIST "})


    if isinstance(request.data['obj_id'], int) and isinstance(request.data['obj_type'], str):
         obj_id = request.data['obj_id']
         obj_type = request.data['obj_type']

    else:
        return Response({"ERROR":"OBJ_ID MUST BE INT ----AND----OBJ_TYPE MUST BE STRING"})

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS:
         model = eval(obj_type)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    else:
         return Response({"error:": "input model does not in MODELS"})
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
         obj = model.objects.get(pk=obj_id)
    except:
         return Response({"ERROR:": "mahsouli ba in moshakhasat vojod nadarad"})

    if obj.stock <= 0 :
         return Response({"ERROR": "OVER PRODUCT STOCK "})

    # تا اینجا اغلب فقط چک کردن بود
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    basket, created = Basket.objects.get_or_create(user=request.user, status='active')
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ct = ContentType.objects.get(model=obj_type.lower())
    basket_item,created = basket.basketitem_set.get_or_create(content_type=ct, object_id=obj_id)
    if  basket_item.count >= obj.stock:
        return Response({"ERROR": "OVER PRODUCT STOCK "})

    basket_item.count += 1
    basket_item.price += obj.price
    basket_item.discount+=obj.discount
    basket_item.save()

    basket.total_price +=obj.price
    basket.total_discount+=obj.discount
    basket.total_discount_price +=(obj.price - obj.discount)
    basket.save()
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # obj.stock -= 1
    # obj.save()  #??????????????????????????????????????????? این خط و خط بالاییش نمیدونم درست هست یا نه

    # ser = BasketItemSerializer(basket_item)
    # return Response(ser.data)
    basket = Basket.objects.filter(status='active', user=request.user)
    ser = BasketSerializer(basket, many=True)
    return Response(ser.data)




@api_view(['PUT'])#فکر کنم باید این رو بزارم put ؟؟
@permission_classes((IsAuthenticated,))
def reduce_basket_item(request):
    try:
        obj_id = request.data['obj_id']
        obj_type = request.data['obj_type']
    except:
        return Response({"ERROR:": "ID OR MODEL DOES NOT EXIST "})

    if isinstance(request.data['obj_id'], int) and isinstance(request.data['obj_type'], str):
        obj_id = request.data['obj_id']
        obj_type = request.data['obj_type']
    else:
        return Response({"ERROR": "OBJ_ID MUST BE INT ----AND----OBJ_TYPE MUST BE STRING"})
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS :
        model = eval(obj_type)
    else:
        return Response({"error:": "input model does not in MODELS"})

    try:
        obj = model.objects.get(pk=obj_id)
    except:
          return Response({"ERROR :":"THIS PRODUCT DOES NOT EXIST"})

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        basket = Basket.objects.get(user=request.user, status='active')
    except:
        return Response({"ERROR:": "YOU DONT HAVE ANY BASKET"})
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        ct = ContentType.objects.get(model=obj_type.lower())
        item = basket.basketitem_set.get(content_type=ct, object_id=obj_id)
        # obj.stock += 1
        # obj.save()

        per_price=item.price / item.count
        discount=item.discount/item.count
        item.count -= 1
        item.price -=per_price
        item.discount -= discount
        basket.total_price -=per_price
        basket.total_discount -=discount
        basket.total_discount_price =basket.total_price - basket.total_discount
        basket.save()
        item.save()

        if item.count <= 0:
            item.delete()
            if basket.basketitem_set.count() <= 0:
                basket.delete()
            #ser=BasketItemSerializer(data=basket.basketitem_set.all(),many=True)
            #return Response(ser.data)
        basket = Basket.objects.filter(status='active', user=request.user)
        ser = BasketSerializer(basket, many=True)
        return Response(ser.data)
    except:
        return Response({"ERROR:": "YOU DONT HAVE THIS ITEM IN YOUR BASKET"})



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_basket(request):
        basket= Basket.objects.filter(status='active',user=request.user)
        ser = BasketSerializer(basket,many=True,context={'request':request})
        return Response(ser.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_favorites(request):
    basket,created=Basket.objects.get_or_create(user=request.user,status='favorites')
    items=basket.basketitem_set.all()
    paginator=PageNumberPagination()
    pagination_items=paginator.paginate_queryset(items,request)
    ser=FavoritesItemSerializer(pagination_items,many=True)
    return Response(ser.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_reduce_favorites(request):
    if request.method=='POST':
        try:
            obj_id=request.data['obj_id']
            obj_type=request.data['obj_type']
        except:
            return Response({"ERROR":"''obj_id' ya 'obj_type' vared nashode"})

        if not( isinstance(obj_type,str) and isinstance(obj_id,int)):
            return Response({"ERROR":"'OBJ_ID' MUST INT  AND 'OBJ_TYPE' MUST BE STR"})

        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        if obj_type in MODELS:
            model=eval(obj_type)
        else:
            return Response({"ERROR":"OBJ_TYPE ISNT IN MODELS"})

        try:
            obj=model.objects.get(pk=obj_id)
        except:
            return Response({"ERROR":"WE DONT HAVE THIS PRODUCT"})

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        f_basket, created =Basket.objects.get_or_create(user=request.user,status='favorites')
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        try:
            ct=ContentType.objects.get(model=obj_type.lower())
            item=f_basket.basketitem_set.get(object_id=obj_id, content_type=ct)

        except:
            ct = ContentType.objects.get(model=obj_type.lower())
            item=f_basket.basketitem_set.create(content_type=ct,object_id=obj_id)
            item.count=1
            item.save()
            return Response({"MESSAGE":"ITEM EZAFE SHOD"})

        item.count=0
        item.delete()
        return Response({"MESSAGE":"ITEM HAZF SHOD"})



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def my_comments(request):
    comments=Comment.objects.filter(user=request.user)
    paginator=PageNumberPagination()
    pagination_comments=paginator.paginate_queryset(comments,request)
    ser = CommentSerializer(pagination_comments,many=True)
    return Response(ser.data)


@api_view(['DELETE','GET'])
@permission_classes((IsAuthenticated,Comment_Owner))
def delete_comment(request,pk):

    # if request.GET.get('obj_type') and request.GET.get('obj_id'):
    #
    #     obj_type=request.GET.get('obj_type')
    #     obj_id=request.GET.get('obj_id')
    #
    # else:
    #     return Response({"error":"'obj_id' ya 'obj_type' dorost vared nashode "})
    #
    # if not(isinstance(obj_type, str)) or not(obj_id.isdigit()):
    #     return Response({"ERROR": "'OBJ_ID' MUST INT  AND 'OBJ_TYPE' MUST BE STR"})
    #
    # MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    # if obj_type in MODELS:
    #     model = eval(obj_type)
    # else:
    #     return Response({"ERROR": "OBJ_TYPE ISNT IN MODELS"})
    #
    # try:
    #     obj = model.objects.get(pk=int(obj_id))
    # except:
    #     return Response({"ERROR": "WE DONT HAVE THIS PRODUCT"})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # obj_id=request.GET.get("obj_id")
    # obj_type=request.GET.get("obj_type")
    # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ct=ContentType.objects.get(model=obj_type.lower())
    comment=Comment.objects.get(user=request.user,pk=pk)

    if request.method=='GET':
        ser=CommentSerializer(comment)
        return Response(ser.data)

    elif request.method=='DELETE':
        comment.delete()
        return Response({"message":"delete shod"})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ct=ContentType.objects.get(model=obj_type.lower())
# cm=Comment.objects.filter(content_type=ct,object_id=obj_id)
# ser=ComentSerializer(cm,many=True)
# if ser.is_valid:
#     return Response(ser.data)

# ser=AddCommentSerializer(data=request.data)
# if ser.is_valid():
#     ser.save()
#     return Response(ser.data)
#     pass##########################################نیاز به تکمیل شدن
# else:
#     return Response(ser.errors)



@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated,Comment_Owner,PublishPermission))
def update_comment(request,pk):
    # import ipdb; ipdb.set_trace()
    # try:
    #     obj_type=request.Get.get('obj_type')
    #     obj_id=request.Get.get('obj_id')
    # except:
    #     return Response({"ERROR": "''obj_id' ya 'obj_type' vared nashode"})
    #
    # if not(isinstance(obj_type, str)) or not(obj_id.isdigit()):
    #     return Response({"ERROR": "'OBJ_ID' MUST INT  AND 'OBJ_TYPE' MUST BE STR"})
    #
    # MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    # if obj_type in MODELS:
    #     model = eval(obj_type)
    # else:
    #     return Response({"ERROR": "OBJ_TYPE ISNT IN MODELS"})
    #چون قبلا کامنت گذاشته فرد پس قطعا چنین موردی وجود داره و نیاز نیست دوباره چک کنیم ببینیم چنین کالایی داریم یا نه و ....پس من بالایی ها رو کامنت می کنم

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # obj_id = request.GET["obj_id"]
    # obj_type = request.GET["obj_type"]
    # ct=ContentType.objects.get(model=obj_type.lower())
    # comment=Comment.objects.get(user=request.user,content_type=ct,object_id=int(obj_id),pk=pk)

    comment = Comment.objects.get(pk=pk)
    if request.method=='GET':
        ser=CommentSerializer(comment)
        return Response(ser.data)

    elif  request.method=='PUT':
        ct=comment.content_type
        obj_id=comment.object_id
        basket_item = BasketItem.objects.filter(content_type=ct, object_id=int(obj_id),
                                                basket__user=request.user, basket__delivered=True)

        if bool(basket_item) == True:
            buyer = True
        else:
            buyer = False
        ser=AddComment2Serializer(comment,data=request.data,context={'buyer':buyer})
        if ser.is_valid():
            ser.save()
            return Response({'message':'sabt shod'})
        else:
            return Response(ser.errors)



@api_view(['POST'])
@permission_classes((IsAuthenticated,JustOneComment))
def add_comment(request):
    obj_id=request.GET.get("obj_id")
    obj_type=request.GET.get("obj_type")
    ct=ContentType.objects.get(model=obj_type.lower())
    basket_item=BasketItem.objects.filter(content_type=ct,object_id=int(obj_id),
                                     basket__user=request.user,basket__delivered=True)#@@@@@@@@@@@@@@@@@@

    if bool(basket_item)==True:
        buyer=True
    else:
        buyer=False

    ser=AddComment2Serializer(data=request.data,context={'buyer':buyer})
    if ser.is_valid():
        ser.save(user=request.user,content_type=ct, object_id=int(obj_id), buyer=buyer)
        # return Response(ser.data)
        return Response({"MESAGE":"SAVE SHOD"})

    else:
        return Response(ser.errors)



@api_view(['POST'])
@permission_classes((IsAuthenticated,IsNotOwner))
def like_comment(request,pk):
    try:
        lk=request.data['like']
        lk=int(lk)
    except:
        return Response({"error":"like must be int-----like -1 ya 1 ast "})

    cmnt = Comment.objects.get(pk=pk)

    try:
        like=Like.objects.get(user=request.user,comment=cmnt)
    except:
        if lk == -1:
            Like.objects.create(user=request.user,comment=cmnt,dislike=True)
            cmnt.count_dislike+=1
            cmnt.save()
            return Response({"message": "sabt shod"})
        elif lk == 1:
            Like.objects.create(user=request.user, comment=cmnt,like=True)
            cmnt.count_like += 1
            cmnt.save()
            return Response({"message": "sabt shod"})
        else:
            return Response({"error": "like must only 1 or -1"})


    if lk==-1:
        if like.dislike==True:
            cmnt.count_dislike-=1
            cmnt.save()
            like.delete()
            return Response({'message':'sabt shod'})

        else:
            like.dislike=True
            like.like=False
            like.save()
            cmnt.count_like-=1
            cmnt.count_dislike+=1
            cmnt.save()
            return Response({'message':'sabt shod'})

    elif lk==1:
        if like.like==True:
            cmnt.count_like-=1
            cmnt.save()
            like.delete()
            return Response({'message':'sabt shod'})
        else:
            like.like=True
            like.dislike=False
            like.save()
            cmnt.count_dislike -= 1
            cmnt.count_like += 1
            # cmnt.most_liked = cmnt.count_like - cmnt.count_dislike
            cmnt.save()
            return Response({'message':'sabt shod'})

    else:
        return Response({"ERROR":"DADEHA MOTABAR NEMIIBASHAD ----LIKE MUST -1 OR 1 "})





@api_view(['GET'])
def show_comment(request):
    # import ipdb; ipdb.set_trace()
    if request.GET.get('obj_type') and request.GET.get('obj_id'):
        obj_type=request.GET.get('obj_type')
        obj_id=request.GET.get('obj_id')
    else:
        return Response({"error":"'obj_id' ya 'obj_type'  vared nashode "})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS:
       model=eval(obj_type)
    else:
        return Response({"error": "obj_type dar MODELS vojod nadarad"})

    try:
        product=model.objects.get(pk=obj_id)
    except:
        return Response({"error":"in mahsol vojod nadarad"})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ct=ContentType.objects.get(model=obj_type.lower())
    if request.GET.get('order')=='newest-comment':
        cm = Comment.objects.filter(content_type=ct, object_id=int(obj_id)).order_by('-write_date')
    elif request.GET.get('order')=='most-liked':
        cm = Comment.objects.filter(content_type=ct, object_id=obj_id)
        cm=sorted(cm, key=lambda i: i.most_liked,reverse=True)#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$property$$$$$$$$$$$$$$$$$$$$$$$$====cm=sorted(cm, key=lambda cm: -cm.most_liked)

    elif request.GET.get('order')=='buyers':#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        cm1=Comment.objects.filter(content_type=ct, object_id=obj_id,buyer=True)
        cm2=Comment.objects.filter(content_type=ct, object_id=obj_id,buyer=False)
        cm=cm1 | cm2

    else:
        return Response({"error":"order ra moshakhas konid"})

    ser=CommentSerializer1(product,context={'comments':cm,'request': request})#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$خیلی خیلی مهم توجه کن خوب--> خود محصول و کامنت هاش
    return Response(ser.data)




#
# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def show_orders(request):
#     basket=Basket.objects.filter(user=request.user)
#     if request.GET.get('type'):
#         type=request.GET.get('type')
#         status=['canceled','deliverd','current']
#
#         if not(type in status):
#             return Response({"ERROR":"STATUS RA DOROST VARED KONID"})
#
#         elif  type == 'current':
#             order1 = Basket.objects.filter(status='pardakht').order_by('-order_registration_date')
#             order2 = Basket.objects.filter(status='pardakht-shod').order_by('-order_registration_date')
#             order = order1 | order2  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
#         else:
#             order = Basket.objects.filter(user=request.user, status=type).order_by('-order_registration_date')
#
#     else:
#         order=Basket.objects.filter(user=request.user).exclude(status='active').\
#             exclude(status='favorites').order_by('-order_registration_date')[0:10] #@@@@@@@@@@@@@@@@@@@@
#
#     ser=OrderSerializer(order,many=True)
#     return Response(ser.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_orders(request):
    try:
        type=request.GET['type']  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    except:
        order=Basket.objects.filter(user=request.user).exclude(status='active').exclude(status='favorites').order_by('order_registration_date')[0:10] #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        paginate=PageNumberPagination()
        paginate.page_size=3
        pagination_order=paginate.paginate_queryset(order,request)
        ser =OrderSerializer(pagination_order, many=True)
        return Response(ser.data)

    if type=='current':
        order1=Basket.objects.filter(user=request.user,status='pardakht')
        order2=Basket.objects.filter(user=request.user,status='pardakht-shod')
        order=order1 |order2           # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        order=order.exclude( delivered=True)  #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        paginate = PageNumberPagination()
        paginate.page_size = 3
        pagination_order = paginate.paginate_queryset(order, request)
        ser = OrderSerializer(pagination_order, many=True)
        return Response(ser.data)

    elif type=='delivered':
        order=Basket.objects.filter(user=request.user,delivered=True)
        paginate = PageNumberPagination()
        paginate.page_size = 3
        pagination_order = paginate.paginate_queryset(order, request)
        ser = OrderSerializer(pagination_order, many=True)
        return Response(ser.data)

    elif type=='canceled':
        order = Basket.objects.filter(user=request.user, status='canceled')
        paginate = PageNumberPagination()
        paginate.page_size = 3
        pagination_order = paginate.paginate_queryset(order, request)
        ser = OrderSerializer(pagination_order, many=True)
        return Response(ser.data)

    elif type=='returned':
        order=ReturningBasket.objects.filter(user=request.user)
        paginate = PageNumberPagination()
        paginate.page_size = 3
        pagination_order = paginate.paginate_queryset(order, request)
        ser=ReturnedBasketSerializer(pagination_order,many=True)
        return Response(ser.data)
    else:
        return Response({'error type must be in ["current","delivered","canceled","returned"]'})



@api_view(['GET'])
@permission_classes((IsAuthenticated,YourOrder))
def order_item(request,pk):
    order = Basket.objects.get(pk=pk, user=request.user)
    ser=OrderItemSerializer(order)
    return Response(ser.data)




@api_view(['PUT'])
@permission_classes((IsAuthenticated,AdressRegisterAbility)) #ActiveTrueBasketببین این پرمیشن چیه قبلی نوشتم
def add_delivery_address(request,pk):
    # این pk درواقع id اون بسکت هست
    #همین رو از طریق سرییلایزرم باید بتونم بنویسم که نتونستم به خاطر ست کردن ریلیشن حتما اینو یاد بگیر#
    order=request.GET['order']
    try:
        address_id = request.data['address_id']  # این همون id ادرس هست و با pk بالا فرق داره
        address = Address.objects.get(pk=address_id, profile__user=request.user)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ profile__user
    except:
        return Response({"error": "id address ra vared konid---or----in address motealegh be shoma nist"})

    if order=='buy':
        basket = Basket.objects.get(user=request.user, pk=pk)
        basket.address = address  # ادرس  فیلد ریلیشن هست همون فوریجن کی@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        basket.save()
        BS=basket

    elif order=='returned':

        return_basket=ReturningBasket.objects.get(pk=pk,user=request.user)
        return_basket.address=address
        return_basket.save()
        BS=return_basket

    data = {"address": BS.address.mailing_address,
            "province": BS.address.province,
            "cily": BS.address.city,
            "unit": BS.address.unit,
            "number": BS.address.number,
            "reciver_first_name": BS.address.reciver_first_name,
            "reciver_first_name": BS.address.reciver_first_name}
    return Response(data)  # خودم دیتا نشون میدم به جا یسریالایزر@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_question(request):
    try:
        obj_id=request.GET['obj_id']
        obj_type=request.GET['obj_type']
    except:
        return Response({"ERROR":"obj_id , obj_type ra vared konid "})

    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS:
        ct=ContentType.objects.get(model=obj_type.lower())
        model=eval(obj_type)
        product=model.objects.get(pk=int(obj_id))
    else:
        return Response({"ERROR":"WE DONT HAVE THIS MODEL--or---this product"})

    # question=Question.objects.create(user=request.user,content_type=ct,object_id=int(obj_id))
    ser=QuestionSerializer(data=request.data)
    if ser.is_valid():
        ser.save(user=request.user,content_type=ct,object_id=int(obj_id))
        return Response(ser.data)
    else:
        return Response(ser.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_reply(request):
    try:
        id=request.GET['id']
        id=int(id)
        question=Question.objects.get(pk=id)
        # import ipdb; ipdb.set_trace()
        product=question.content_object
    except:
        return Response({"ERROR":"ID COMMENT VARED NASHODE---OR--IN QUESTION VOJOD NADARAD"})


    ser=ReplyQuestionSerializer(data=request.data)#خیلی مهم@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    if ser.is_valid():
        ser.save(user=request.user,question=question)
    else:
        return Response(ser.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like_dislike_reply(request):
    try:
        id=request.GET['id']
        reply_obj=Reply.objects.get(pk=int(id))
    except:
        return Response({"ERROR":"ID VARED KONID---or---in reply vojod nadatad"})
    try:
       # import ipdb; ipdb.set_trace()
       like=request.data['like']
       lk = int(like)
       if not(lk in[1,-1]):
           return Response({"ERROR":"LIKE MUST '-1' OR '1'"})

    except:
        return Response({"ERROR":"LIKE RA VARED KONID.LIKE MUST '-1' OR '1'"})

    try:
        # import ipdb; ipdb.set_trace()
        lk_ins=Like.objects.get(user=request.user,reply=reply_obj)


    except:
        if lk==-1:
             Like.objects.create(user=request.user,reply=reply_obj,dislike=True)

             reply_obj.count_dislike+=1
             reply_obj.save()

        elif lk==1:
            Like.objects.create(user=request.user, reply=reply_obj, like=True)

            reply_obj.count_like += 1
            reply_obj.save()
        return Response({"MESSAGE":"SABT SHOD"})


    if lk==1 :
        if lk_ins.like==True:
            lk_ins.delete()
            reply_obj.count_like -=1
            reply_obj.save()
        if lk_ins.dislike==True:
            lk_ins.delete()
            Like.objects.create(user=request.user, reply=reply_obj, like=True)
            reply_obj.count_like +=1
            reply_obj.count_dislike -= 1
            reply_obj.save()


    if lk==-1:
        if lk_ins.dislike==True:
            lk_ins.delete()
            reply_obj.count_dislike -=1
            reply_obj.save()
        if lk_ins.like==True:
            lk_ins.delete()
            Like.objects.create(user=request.user, reply=reply_obj, dislike=True)
            reply_obj.count_like -= 1
            reply_obj.count_dislike += 1
            reply_obj.save()
    return Response({"MESSAGE":"SABT SHOD"})

@api_view(['GET'])
def show_quesstion_reply(request):
    try:

        obj_id=request.GET['obj_id']
        obj_type=request.GET['obj_type']
        obj_product=eval(obj_type).objects.get(pk=int(obj_id))

    except:
        return Response({"ERROR":"OBJ_ID OR OBJ-TYPE DOROST VARED NASHODE"})

    #ORDER=[NEWEST/////MOST_ANSWERS//////USERS_QUESTION_ONLY
    # import ipdb; ipdb.set_trace()
    questions=Question.objects.filter(content_type=ContentType.objects.get_for_model(obj_product),
                            object_id=obj_product.id)
    ser=ShowQuestionSerializer(questions,many=True,context={'questions':questions})
    return Response(ser.data)



@api_view(['PUT'])
@permission_classes((IsAuthenticated,ActiveTrueBasket))
def add_delivery_date(request,pk):
    #pk مربوط به بسکت
    try:
        date = request.data['date']
        time_range = request.data['time_range']
        if  not(time_range in ['A','B','C','D']):
            return Response({"error":"time_range is in ['A','B','C','D']"})
    except:
        return Response({"ERROR": "date va time_range ra vered konid"})


    date_range = [datetime.date.today() + datetime.timedelta(i) for i in range(1, 6)]  # @@@@@@@@@@@@@@@@@@@@@@@@@@
    try:

        date = datetime.datetime.strptime(date,'%Y-%m-%d').date()  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    except:
        return Response({'error': 'date ra be dorost vared konid'})

    if date in date_range:
        time, created = DeliveryDate.objects.get_or_create(date=date, time_range=time_range)
    else:
        return Response({'error': 'date bayat beyn emroz ta 5 roze ayande bashad '})


    basket = Basket.objects.get(user=request.user, pk=pk)
    if bool(basket.deliverydate)==True:
        previous_delivery_date=basket.deliverydate
        previous_delivery_date.capacity -=1
        previous_delivery_date.save()
        basket.deliverydate=None#@@@@@@@@@@@@@@@@@@@@@@@@None
        basket.save()

    ser=DeliveryDateSerializer(time,data=request.data)
    if ser.is_valid() :
       ser.save()
       basket.deliverydate=time
       basket.save()
       return Response(ser.data)
    else:
           return Response(ser.errors)



@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated,CancelledTimeLimit))
def cancel_item_or_basket(request,pk):
    # pk برای بسکت خرید هست
    basket = Basket.objects.get(pk=pk, user=request.user)
    basket_items = basket.basketitem_set.all()
    if request.method=='GET':
        ser=BasketItemSerializer(basket_items,many=True)
        return Response(ser.data)

    if request.method=='PUT':
        if bool(request.data.get("all_items","")): #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            items = basket.basketitem_set.all()
            try:
                reason=request.data['reason']

            except:
                return Response({'error':'reason ra vared konid'})

            refund_amount=0
            for basket_item in basket_items:
                refund_amount += (basket_item.price - basket_item.discount)
                basket_item.content_object.stock+=basket_item.count #@@@@@@@@@@@@@@@@@@@@@@@@@@
                basket_item.content_object.save() #@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                cancel_cause,created=CauseOfCancalation.objects.get_or_create(content_type=basket_item.content_type,
                                                            object_id=basket_item.object_id,reason=reason)#@@@@@@@@@@@@
                cancel_cause.count += 1
                cancel_cause.save()

                basket.status='canceled'
                basket.save()

            RefundAmount.objects.create(basket=basket,status='C',amount=refund_amount)
            if basket.deliverydate:
                basket.deliverydate.capacity -=1
                basket.deliverydate.save()

            return Response({"mesage":"sabt shod"})

        elif bool(request.data.get("obj_list","")):
            #{"obj_list": [ {"id":1,"type":"red"}, {"id":2,"type":"zard"}, {"id":3,"type":"abi"}  ]}
            items=request.data.get("obj_list")#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            basket=Basket.objects.get(pk=pk)

            #با سریالایزر هم میشه پایینی ها رو نوشت ؟چهطور یمیشه؟
            for item in items:
                # basket.basketitem_set.all().get(pk=item['id'])
                try:
                    id=item['id']
                    count=item['count'] #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                    reason=item['reason']
                except:
                    return Response({'error':'id ,count,reason vared shavad baray har item'})

                try:
                    basket_item=BasketItem.objects.get(pk=id)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                except:
                    return Response({'error':'chenin basket_itemi vojod nadarad'})


                if not(basket_item in basket_items):
                    return Response({'error':'in basket_item  dar in sabad kharid shoma nist'})

                if count>basket_item.count:
                    return Response({"ERROR":"COUNT bishtar az tedad dar basket shoma"})

            refund_amount = 0
            for item in items:
                id=item['id']
                count=item['count']
                reason=item['reason']
                basket_item = BasketItem.objects.get(pk=id)
                # import ipdb; ipdb.set_trace()
                refund_amount += ((basket_item.price-basket_item.discount)/basket_item.count)*count

                cancel_cause, created = CauseOfCancalation.objects.get_or_create\
                    (content_type=basket_item.content_type, object_id=basket_item.object_id, reason=reason)
                cancel_cause.count += 1
                cancel_cause.save()

                basket_item.content_object.stock += count
                basket_item.content_object.save()

                price= count * (basket_item.price/ basket_item.count)
                basket_item.price -= price
                basket.total_price -= price
                discount=count * (basket_item.discount/ basket_item.count)
                basket_item.discount -= discount
                basket.total_discount -=discount
                basket_item.count -= count
                basket.total_discount_price=basket.total_price - basket.total_discount
                # basket_item.discount_price =basket_item.price -  basket_item.discount
                basket_item.save()
                basket.save()
                if basket_item.count==0:
                    basket_item.delete()


            RefundAmount.objects.create(basket=basket,status='C',amount=refund_amount)
            if basket.basketitem_set.count()==0:
                # basket.delete()#نمیشه چون وقتی این از بین بره تمام وابسته هاش مثل هزینه مرجوعی هم  از بین میره
                basket.status="canceled"
                basket.save()

            return Response({"mesage": "sabt shod"})

        else:
            return Response({'error':'"all_items" ya "obj_list" zarori ast'})



@api_view(['GET'])
@permission_classes((IsAuthenticated,YourReturnBasket))
def show_returning_basket(request,pk):
    returning_basket=ReturningBasket.objects.get(pk=pk,user=request.user)
    ser=ReturningBasketSerializer(returning_basket)
    return Response(ser.data)



@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated,AllowCancelledReturnBasket))
def canceled_returning_basket(request,pk):
         returning_basket = ReturningBasket.objects.get(pk=pk)
         reterning_item = returning_basket.returningitem_set.all()
         if request.method=='GET':
             ser=ReturningBasketSerializer(returning_basket)
             return Response(ser.data)
         if request.method=='PUT':
            try:
                message=request.data['message']
                if message !='canceled':
                    return Response({'error':'payam dorost vared nashode'})
            except:
                return Response({'error':'message daryaft nashod'})


            returning_basket.status='canceled'
            returning_basket.save()

            for item in reterning_item:
               item.status = 'canceled'
               item.save()

            if bool(returning_basket.returning_date):
                returning_basket.returning_date.capacity -=1
                returning_basket.returning_date.save()

                returning_basket.returning_date=None
                returning_basket.save()

            if bool(returning_basket.address):
                returning_basket.address=None
                returning_basket.save()

            ser=ReturningBasketSerializer(returning_basket)
            return Response(ser.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,AllowedToSet))
def add_returning_date(request,pk):
    #pk بسکت مرجوعی است
    try:
        date=request.data['date']
        time_range=request.data['time_range']
        if  not(time_range in ['A','B']):
            return Response({'error':'time_range in["A","B"] ast'})
    except:
        return Response({'error':'date va time_range ra vared konid'})

    return_basket = ReturningBasket.objects.get(pk=pk, user=request.user)
    # date_range=[return_basket.basket.deliverydate.date + datetime.timedelta(i) for i in range(1,8)] #@@@@@@@@@@@@@@@@
    date_range=[datetime.date.today()+datetime.timedelta(i) for i in range(1,6)]
    try:
        date=datetime.datetime.strptime(date,'%Y-%m-%d').date()#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    except:
        return Response({'error':'date ra be forrmat dorost vared konid'})

    if not(date in date_range):
        return Response({'error':'date bayad az farda ta 5 roz ayande bahad'})

    # import ipdb; ipdb.set_trace()
    return_time, created = ReturningDate.objects.get_or_create(returning_date=date, time_range=time_range)
    if not (return_time.available):
        return Response({'error': 'in baze por shode va  capacity nadarad'})


    if bool(return_basket.returning_date) ==True:
        old_date_time=return_basket.returning_date
        old_date_time.capacity -=1
        old_date_time.save()
        return_basket.returning_date=None
        return_basket.save()


    return_time.capacity+=1
    return_time.save()
    return_basket.returning_date=return_time
    return_basket.save()
    return Response({'message':'sabt shod','date':date,'time_range':time_range})




@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,ReturnTimeLimit,HaveInactiveReturningBasket))
def add_returning_items(request,pk):
    #pk اون بسکت اصلی هست
    basket = Basket.objects.get(pk=pk, user=request.user)
    basket_items = basket.basketitem_set.all()
    if request.method=='GET':
        ser=BasketItemSerializer(basket_items,many=True)
        return Response(ser.data)

    if request.method=='POST':
        try:
           items=request.data['obj_list']
           if bool(items)==False:
               return Response({'error': 'obj_list khali ast'})
        except:
            return Response({'error':'obj_list vared shavad'})
            # BasketItem.objects.get(pk=item['basket_item'],basket__user=request.user)

        for item in items:
            try:
                id=item['basket_item']
                count=item['count']
                reason=item['reason']
                descriptions=item['descriptions']
                itm=basket.basketitem_set.get(pk=id)
                if count>itm.count:
                    return Response({'error':'count nabayad bish az tedad dar basket shoma bashad'})
            except:
                return Response({'error':'basket_item,count,reason ra be dorosti varedkonid'})


        returning_basket=ReturningBasket.objects.create(user=request.user,basket=basket,status='active',
                                                registration_date=datetime.date.today()) # status='accepted'هم باید بتونه باشه چی کار کنم؟؟؟؟؟

        refund_amount=0
        for item in items:
            ser=AddReturnItemSerializer(data=item)
            if ser.is_valid():
                bs_item=BasketItem.objects.get(pk=item['basket_item'])
                # refund_amount+=(bs_item.price/bs_item.count)*item['count']
                ser.save(basket_item=bs_item,returning_basket=returning_basket,status='active')

            else:
                returning_basket.delete()
                return Response(ser.errors)

        # RefundAmount.objects.create(basket=basket,status='returned',amount=refund_amount)
        return Response({'message':'zakhireh shod'})
        #ایا باید به استاک اینجا اضافه بشه چون ممکنه لغو کنه دوباره مرجوعیش رو؟فعلا این قسمت رو ننوشتم



@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated,HaveActiveReturningBasket))
def edite_returning_items(request,pk):
    # pk اون بسکت اصلی هست
    basket = Basket.objects.get(pk=pk, user=request.user)
    basket_items = basket.basketitem_set.all()

    return_basket = basket.returningbasket_set.all().exclude(status="canceled").exclude(status="received").first()
    return_items = [i.basket_item for i in return_basket.returningitem_set.all().exclude(status='canceled')]  # $$$$$$$$$$$$$$$$$$$$$$$$$$$

    if request.method=='GET':
        ser=BasketItemSerializer(return_items,many=True)
        return Response(ser.data)

    if request.method=='PUT':


        try:
            items = request.data['obj_list']
        except:
            return Response({'error': 'obj_list vared shavad'})
            # BasketItem.objects.get(pk=item['basket_item'],basket__user=request.user)

        for item in items:
            try:
                id = item['basket_item']
                delete = item['delete']
                itm = basket.basketitem_set.get(pk=id)
                if not(itm in return_items) :
                    return Response({'error':'chenin itemi dar returning_basket shoma vojod nadarad'})

            except:
                return Response({'error': 'basket_item, delete dorost vared konid'})


        for item in items:
                if item['delete']=='true':
                    itm = basket.basketitem_set.get(pk=item['basket_item'])
                    return_item=ReturningItem.objects.get(returning_basket=return_basket,basket_item=itm)
                    # return_item=return_items.objects.get(basket_item=bs_item)
                    return_item.status="canceled"
                    return_item.save()


                elif item['delete']=='false':

                    try:
                        itm = basket.basketitem_set.get(pk=item['basket_item'])
                        count = item['count']
                        reason = item['reason']
                        descriptions = item['descriptions']
                        if count > itm.count or count==0:
                            return Response({'error': 'count nabayad bish az tedad dar basket shoma bashad-va nabayad sefr bashad'})
                    except:
                        return Response({'error':',count,reason ,descriptions ra be dorosti  vared konid'})

                    # bs_item=BasketItem.objects.get(pk=item['basket_item'])
                    return_item = ReturningItem.objects.get(returning_basket=return_basket, basket_item=itm)
                    ser=AddReturnItemSerializer(return_item,data=item)

                    if ser.is_valid():
                        ser.save(status="active")
                    else:
                        return Response(ser.errors)

                else:
                    return Response({'error':'delete must "true" or "false" '})

                # return_items=return_basket.returningitem_set.all()
                # for i in return_items:
                #     active=0
                #     if i.status=="active" or i.status=="accepted" :
                #         active+=1
                #         break
                #
                # if active==0:
                #     return_basket.status="canceled"
                #     return_basket.save()
                #     if return_basket.returning_date:
                #         return_basket.returning_date.capacity -=1
                #         return_basket.returning_date.save()
                #     if return_basket.address:
                #         return_basket.address==None
                #         return_basket.save()
                #
                #     return Response({'message':'sabt shod'})
                # else:
                #     return Response({'message': 'sabt shod'})

        return Response({'message': 'sabt shod'})







   #
   # main_api='https://raygansms.com/SendMessageWithUrl.ashx?'
   # url=main_api + urllib.parse.urlencode({'Username':'09123669277','Password':'5989231',
   #                                        'PhoneNumber':'50002910001080','MessageBody':'سلام خوبی؟ فهیمه فرزانه',
   #                                        'RecNumber':'09123669277','Smsclass':'1'})
   #
   #
   # json_data=requests.get(url).json()#مهمه
   #
   # # print(json_data)
   #
   # return Response({'hh':'aa'})

@api_view(['POST'])
@permission_classes((MustAnonymouse,))
def login_register(request):
       
       mobile=str(request.data['mobile'])
       rand =str(random.randrange(1000, 10000))
       message=f' کد اعتباری سنجی شما : {rand}'
       user,create=User.objects.get_or_create(username=mobile)
       user_validation,create=ValidationCode.objects.get_or_create(user=user)
       user_validation.validation_code=rand
       user_validation.save()

       main_api='https://raygansms.com/SendMessageWithUrl.ashx?' #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
       url=main_api + urllib.parse.urlencode({'Username':'09123669277','Password':'5989231',
                                              'PhoneNumber':'50002910001080','MessageBody':message,
                                              'RecNumber':mobile,'Smsclass':'1'}) #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
       json_data = requests.get(url).json() #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
       return Response({'message':'کد اعتبارسنجی برای شما ارسال شد.ان را وارد کنید'})


@api_view(['POST'])
@permission_classes((MustAnonymouse,))
def confirm_code(request):
    try:
        mobile=str(request.data['mobile'])
        code=str(request.data['code'])
        user_code = ValidationCode.objects.get(user__username=mobile).validation_code
        user=User.objects.get(username=mobile)
    except:
        return Response({"ERROR":"mobile or code vared nashode"})

    if user_code==code:
        token, create = Token.objects.get_or_create(user=user)
        return Response({'Token':token.key})

    else:
        return Response({'error':'error'})


















   

   
    

    



