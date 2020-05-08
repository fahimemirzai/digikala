from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers, BasketItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app_accounts.permissions import IsOwner
from .models import BasketItem, Basket
from app_product.models import Cellphone, Tablet, Laptop, Television
from django.contrib.contenttypes.models import ContentType


@api_view(['POST'])
def register(request):
    ser = UserSerializers(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsOwner))
def ProfileView(request):
    try:
        user = User.objects.get(username=request.query_params['username'])
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
def show_basket_item(request):
    basket_item = BasketItem.objects.filter(basket__user=request.user, basket__status='active')
    ser = BasketItemSerializer(basket_item, many=True)
    return Response(ser.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_basket_item(request):
    try:
        obj_id = request.data['obj_id']
        obj_type = request.data['obj_type']
        isinstance(obj_id, int) and isinstance(obj_type, str)
    except:
        return Response({"ERROR:":"ID OR MODEL DOES NOT EXIST .OR INVALID INPUT"})


    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS:
        model=eval(obj_type)
    else:
        return Response({"error:": "input model does not in MODELS"})

    try:
        obj=model.objects.get(pk=obj_id)
        obj.stock>=1
    except:
        return Response({"ERROR:": "THIS PRODUCT NOT EXIST ___OR___ OVER STOCK ERROR"})


    basket,created=Basket.objects.get_or_create(user=request.user,status='active')
    try:
        #import ipdb ; ipdb.set_trace()
        ct=ContentType.objects.get(model=obj_type.lower())
        basket_item=basket.basketitem_set.get(content_type=ct,object_id=obj_id)

    except:
        basket_item = basket.basketitem_set.create(content_type=ct, object_id=obj_id)

    basket_item.count+=1
    basket_item.save()
    #import ipdb ; ipdb.set_trace()
    obj.stock -= 1
    obj.save() #این خط و خط بالاییش نمیدونم درست هست یا نه

    basket_item = BasketItemSerializer(basket_item)
    return Response(basket_item.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reduce_basket_item(request):
    try:
        obj_id = request.data['obj_id']
        obj_type = request.data['obj_type']
        isinstance(obj_id, int) and isinstance(obj_type,str)
    except:
        return Response({"ERROR:": "ID OR MODEL DOES NOT EXIST .OR INVALID INPUT"})

    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    if obj_type in MODELS :
        model = eval(obj_type)
    else:
        return Response({"error:": "input model does not in MODELS"})

    try:
        obj = model.objects.get(pk=obj_id)##
    except:
          return Response({"ERROR :":"THIS PRODUCT NOT EXIST"})


    try:
        basket = Basket.objects.get(user=request.user,status='active')##

    except:
        return Response({"ERROR:": "YOU DONT HAVE ANY BASKET"})


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
    except:
        return Response({"ERROR:": "YOU DONT HAVE THIS ITEM IN YOUR BASKET"})


"""
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_basket_view(request):
    MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
    obj_id = request.data['obj_id']
    obj_type = request.data['obj_type']

    basket, created = Basket.objects.get_or_create(user=request.user, status='active')

    # try:
    #     basket = Basket.objects.filter(user=request.user, on_off=True)[0]
    # except:
    #     basket = Basket.objects.create(user=request.user)
    #     basket.save()

    if obj_type in MODELS:
        model = eval(obj_type)
        obj = model.objects.get(pk=obj_id)
        import ipdb ; ipdb.set_trace()

        try:
            basket_item=BasketItem.objects.get(basket=basket, content_object=obj)
            #basket_item = BasketItem.objects.get(basket=basket, content_type=ct, object_id=obj_id)
            ###  basket_item = basket.basketitem_set.get(content_type=ct, object_id=obj_id)

        except:
            basket_item = BasketItem.objects.create(basket=basket, content_object=obj)
            ###   basket_item = basket.basketitem_set.create(content_object=obj)
            #basket, created = request.user.basket_set.get_or_create(status='active')

         #ct = ContentType.objects.first()

        # try:
        #     item_basket = BasketItem.objects.filter(basket=basket, content_object=obj)
        # except:
        #     item_basket = BasketItem.objects.create(basket=basket, content_object=obj)

        basket_item.count += 1
        basket_item.save()
        basket_item = BasketItemSerializer(basket_item)
    return Response(basket_item.data)

"""
