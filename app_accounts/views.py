from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers, BasketItemSerializer, BasketSerializer, ProfileSerializer,\
    EditProfileSerializer, UserSerializer2,AddressSerializer,AddAddressSerializer,UpdateAddressSerializer,\
    BasketFavoriteSerializer,CommentSerializer,AddCommentSerializer,AddComment2Serializer,\
    GoodBadPointSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app_accounts.permissions import IsOwner, MustAnonymouse,Comment_Owner,PublishPermission,JustOneComment,IsNotOwner
from .models import BasketItem, Basket, Profile,Address,Comment,Like
from app_product.models import Cellphone, Tablet, Laptop, Television
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
# from passlib.hash import pbkdf2_sha256



@api_view(['POST'])
@permission_classes((MustAnonymouse,))
def register(request):
    ser = UserSerializers(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)


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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    try:
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        repeat_new_password = request.data['repeat_new_password']
    except:
        return Response({"error":" 'old_password' ya 'new_password' ya 'repeat_new_password' ra vared nakarid"})

    if check_password(old_password, request.user.password):
        if new_password == repeat_new_password:
            request.user.password = make_password(new_password)
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
def address(request):
    profile=Profile.objects.get(user=request.user)
    #my_address=Profile.objects.filter(address__profile=user)
    #import ipdb ; ipdb.set_trace()
    addresses=profile.address_set.all()
    ser=AddressSerializer(addresses,many=True)
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


@api_view(['PUT'])
@permission_classes((IsAuthenticated,IsOwner))
def edit_address(request,pk):
    address=Address.objects.get(pk=pk)
    ser=UpdateAddressSerializer(address,data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)


########################################################################

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
        request.data['obj_id'] and  request.data['obj_type']
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
         model = eval(obj_type)
    else:
         return Response({"error:": "input model does not in MODELS"})
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
         obj = model.objects.get(pk=obj_id)
    except:
         return Response({"ERROR:": "THIS PRODUCT NOT EXIST "})

    if obj.stock <= 0:
         return Response({"ERROR": "OVER STOCK PRODUCT"})
    # تا اینجا اغلب فقط چک کردن بود
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    basket, created = Basket.objects.get_or_create(user=request.user, status='active')
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
         ct = ContentType.objects.get(model=obj_type.lower())
         basket_item = basket.basketitem_set.get(content_type=ct, object_id=obj_id)
    except:
         basket_item = basket.basketitem_set.create(content_type=ct, object_id=obj_id)

    basket_item.count += 1
    basket_item.save()
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    obj.stock -= 1
    obj.save()  # این خط و خط بالاییش نمیدونم درست هست یا نه
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    basket_item = BasketItemSerializer(basket_item)
    return Response(basket_item.data)



@api_view(['POST'])#فکر کنم باید این رو بزارم put ؟؟
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
          return Response({"ERROR :":"THIS PRODUCT NOT EXIST"})

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        basket = Basket.objects.get(user=request.user, status='active')
    except:
        return Response({"ERROR:": "YOU DONT HAVE ANY BASKET"})
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        ct = ContentType.objects.get(model=obj_type.lower())
        item = basket.basketitem_set.get(content_type=ct, object_id=obj_id)
        obj.stock += 1
        obj.save()
        
        item.count -= 1
        item.save()

        if item.count <= 0:
            item.delete()
            if basket.basketitem_set.count() <= 0:
                basket.delete()
            #ser=BasketItemSerializer(data=basket.basketitem_set.all(),many=True)
            #return Response(ser.data)

        return Response({"MESSAGE":"REDUCE ITEM FROM YOUR BASKET"})
    except:
        return Response({"ERROR:": "YOU DONT HAVE THIS ITEM IN YOUR BASKET"})





@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_basket(request):
    basket = request.user.basket_set.filter(status='active')
    ser = BasketSerializer(basket, many=True)
    return Response(ser.data)



@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def favorite_basket(request):
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
        return Response({"MESSAGE","ITEM HAZF SHOD"})
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if request.method=='GET':
        f_basket, craeted = Basket.objects.get_or_create(user=request.user, status='favorites')
        items = f_basket.basketitem_set.all()
        ser=BasketFavoriteSerializer(items,many=True)
        return Response(ser.data)

####################################################################################
"""
@api_view(['GET'])
def show_comment(request):
    if request.GET.get('obj_type') and request.GET.get('obj_id'):
        obj_type=request.GET.get('obj_type')
        obj_id=request.GET.get('obj_id')
    else:
        return Response({"error":"'obj_id' ya 'obj_type' dorost vared nashode "})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS:
       model=eval(obj_type)
    else:
        return Response({"ERROR": "OBJ_TYPE ISNT IN MODELS"})

    try:
        model.objects.get(pk=obj_id)
    except:
        return Response({"ERROR":"WE DONT HAVE THIS PRODUCT"})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ct=ContentType.objects.get(model=obj_type.lower())
    cm=Comment.objects.filter(content_type=ct,object_id=obj_id)
    # ser=CommentSerializer(cm,many=True)
    ser=CommentSerializer(cm,many=True)
    return Response(ser.data)
"""

@api_view(['DELETE','GET'])
@permission_classes((IsAuthenticated,Comment_Owner))
def delete_comment(request):

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
    obj_id=request.GET.get("obj_id")
    obj_type=request.GET.get("obj_type")
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ct=ContentType.objects.get(model=obj_type.lower())
    coment=Comment.objects.get(user=request.user,content_type=ct,object_id=int(obj_id))

    if request.method=='GET':
        ser=CommentSerializer(coment)
        return Response(ser.data)
    elif request.method=='DELETE':
        coment.delete()
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
def update_comment(request):
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
    obj_id = request.GET["obj_id"]
    obj_type = request.GET["obj_type"]

    ct=ContentType.objects.get(model=obj_type.lower())
    comment=Comment.objects.get(user=request.user,content_type=ct,object_id=int(obj_id))
    if request.method=='GET':
        ser=CommentSerializer(comment)
        return Response(ser.data)

    elif  request.method=='PUT':

        ser=AddCommentSerializer(comment,data=request.data)
        if ser.is_valid():
            ser.save()
            # return Response(ser.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,JustOneComment))
def add_comment(request):
    obj_id=request.GET.get("obj_id")
    obj_type=request.GET.get("obj_type")

    # import ipdb; ipdb.set_trace()
    # data1={obj_id:int(obj_id),obj_type:obj_type}
    # request.data.update(data1)
    ct=ContentType.objects.get(model=obj_type.lower())
    # ser2 = GoodBadPointSerializer(data=request.data)



    ser=AddComment2Serializer(data=request.data)
    if ser.is_valid():
        ser.save(user=request.user,content_type=ct,object_id=int(obj_id))
        # return Response({"MESAGE":"SAVE SHOD"})
        # return Response(ser.data)#اینم میشه و مشکل نداره و فقط اون ۴ تا فیلد تو سریالایزرش رو نشون میده
    else:
        return Response(ser.errors)






@api_view(['POST'])
@permission_classes((IsAuthenticated,IsNotOwner))
def like_comment(request):
    try:
        id=request.GET.get("id")
        lk=request.data['like']
        # import ipdb; ipdb.set_trace()
        lk=int(lk)

    except:
        return Response({"error":"like must be int-----like -1 ya 1 ast "})
    try:
        cmnt = Comment.objects.get(pk=id)
    except:
        return Response({"ERROR":"COMMENT NOT FOUNT"})
    try:
        like=Like.objects.get(user=request.user,comment=cmnt)
    except:
        if lk == -1:
            Like.objects.create(user=request.user,comment=cmnt,dislike=True)
            cmnt.count_dislike+=1
            cmnt.most_liked=cmnt.count_like-cmnt.count_dislike
            cmnt.save()


            return Response({"message": "sabt shod"})
        elif lk == 1:
            Like.objects.create(user=request.user, comment=cmnt,like=True)
            cmnt.count_like += 1
            cmnt.most_liked = cmnt.count_like - cmnt.count_dislike
            cmnt.save()
            return Response({"message": "sabt shod"})
        else:
            return Response({"error": "like must only 1 or -1"})

    if lk==-1:
        if like.dislike==True:
            return Response({"MESSAGE":"RAY DADIN DAR GOZASHTE"})
        else:
            like.dislike=True
            like.like=False
            like.save()
            cmnt.count_like-=1
            cmnt.count_dislike+=1
            cmnt.most_liked = cmnt.count_like - cmnt.count_dislike
            cmnt.save()
            return Response({"MESSAGE":"SABT SHOD"})

    elif lk==1:
        if like.like==True:
            return Response({"MESSAGE":"RAY DADIN DAR GOZASHTE"})
        else:
            like.like=True
            like.dislike=False
            like.save()
            cmnt.count_dislike -= 1
            cmnt.count_like += 1
            cmnt.most_liked = cmnt.count_like - cmnt.count_dislike
            cmnt.save()
            return Response({"MESSAGE":"SABT SHOD"})

    else:
        return Response({"ERROR":"DADEHA MOTABAR NEMIIBASHAD ----LIKE MUST -1 OR 1 "})







@api_view(['GET'])
def show_comment(request):
    if request.GET.get('obj_type') and request.GET.get('obj_id'):
        obj_type=request.GET.get('obj_type')
        obj_id=request.GET.get('obj_id')
    else:
        return Response({"error":"'obj_id' ya 'obj_type' dorost vared nashode "})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS:
       model=eval(obj_type)
    else:
        return Response({"ERROR": "OBJ_TYPE ISNT IN MODELS"})

    try:
        model.objects.get(pk=obj_id)
    except:
        return Response({"ERROR":"WE DONT HAVE THIS PRODUCT"})
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ct=ContentType.objects.get(model=obj_type.lower())



    if request.GET.get('order')=='newest-comment':
        cm = Comment.objects.filter(content_type=ct, object_id=obj_id).order_by('-write_date')
    elif request.GET.get('order')=='most-liked':
        cm = Comment.objects.filter(content_type=ct, object_id=obj_id).order_by("-most_liked")

        pass
    elif request.GET.get('order')=='buyers':
        pass
    else:
        return Response({"ERROR":"ORDER RA MOSHAKHAS KONID"})


    ser=CommentSerializer(cm,many=True)
    return Response(ser.data)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_orders(request):
    basket=Basket.objects.filter(user=request.user)
    if request.GET.get('type'):
        type=request.GET.get('type')
        status=['canceled','deliverd','current']

        if not(type in status):
            return Response({"ERROR":"STATUS RA DOROST VARED KONID"})

        elif  type == 'current':
            order1 = Basket.objects.filter(status='pardakht').order_by('-order_registration_date')
            order2 = Basket.objects.filter(status='pardakht-shod').order_by('-order_registration_date')
            order = order1 | order2  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        else:
            order = Basket.objects.filter(user=request.user, status=type).order_by('-order_registration_date')

    else:
        order=Basket.objects.filter(user=request.user).exclude(status='active').\
            exclude(status='favorites').order_by('-order_registration_date')[0:10] #@@@@@@@@@@@@@@@@@@@@

    ser=OrderSerializer(order,many=True)
    return Response(ser.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def order_item(request,pk):
    try:
        order=Basket.objects.get(pk=pk)
    except:
        return Response({"error":"we dont have this objects"})

    ser=OrderItemSerializer(order)
    return Response(ser.data)







