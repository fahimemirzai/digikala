from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers, BasketItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app_accounts.permissions import IsOwner
from .models import BasketItem, Basket
from app_product.models import Cellphone, Tablet, Laptop, Television


@api_view(['POST'])
def RegisterView(request):
    ser=UserSerializers(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsOwner))
def ProfileView(request):
    try:
        user=User.objects.get(username=request.query_params['username'])
    except:
        return Response({"ERROR": "WE DONT HAVE THIS USERNAME"})
    else:
        ser=UserSerializers(user)
        return Response(ser.data)


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


################################################################################
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_basket_item_view(request):
    basket_item = BasketItem.objects.filter(basket__user=request.user)
    ser = BasketItemSerializer(basket_item, many=True)
    return Response(ser.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_basket_view(request):
     MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
     obj_id = request.data['obj_id']
     obj_type = request.data['obj_type']
     try:
         basket=Basket.objects.filter(user=request.user, on_off=True)[0]
     except:
         basket = Basket.objects.create(user=request.user)
         basket.save()

     if obj_type in MODELS:
         model = eval(obj_type)
         obj = model.objects.get(pk=obj_id)

         try:
             item_basket = BasketItem.objects.filter(basket=basket, content_object=obj)
         except:
             item_basket = BasketItem.objects.create(basket=basket, content_object=obj)

         item_basket=BasketItemSerializer(item_basket)#######
         item_basket.count+=1
         item_basket.save()




#all_basket_item=BasketItem.objects.all()
"""
##################################### (---reduce---)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reduce_basket_view(request):
    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    obj_id = request.data['obj_id']
    obj_type = request.data['obj_type']

    if obj_type in MODELS:
        model = eval(obj_type)
        obj = model.objects.get(pk=obj_id)
        try:
            item_basket = BasketItem.objects.filter(basket=basket, content_object=obj)
            if item_basket.count >= 1:
                item_basket.count -= 1
                item_basket.save()



        except:
            return Response({"ERROR":"ITEM NOT EXIST IN YOUR BASKET(BASKET ITEM)"})


"""






# def (request):
#     count = request.POST.get('count')
#     object_id = request.POST.get('object_id')
#     content_type = request.POST.get('content_type')

#     basket, created = Basket.objects.get_or_create(user=request.user)
#     basket_item = BasketItem(
#         basket=basket,
#         user=request.user,
#         count=count,
#         content_type=content_type,
#         object_id=object_id,
#     )
#     basket_item.save()





# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def add_basket_view(request):

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@___akhari


@api_view(['POST'])
def add_basket_view(request):
     MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
     obj_id=request.data['obj_id']
     obj_type=request.data['obj_type']
     try:
         basket=Basket.objects.filter(user=request.user,on_off=True)[0]
       
     except:
         basket = Basket.objects.create(user=request.user, on_off=True)
         basket.save()

     if obj_type in MODELS:
         model = eval(obj_type)
         obj = model.objects.get(pk=obj_id)
         item_basket = BasketItem.objects.create(basket=basket, content_object=obj)
         item_basket.save()

"""


