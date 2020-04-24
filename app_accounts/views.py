from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers,Model_Json_Serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app_accounts.permissions import IsOwner


@api_view(['POST'])
def RegisterView(request):

    ser=UserSerializers(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)



@api_view(['GET'])
@permission_classes((IsAuthenticated,IsOwner))
def ProfileView(request):
    try:
            user=User.objects.get(username=request.query_params['username'])
    except:
        return Response({"ERROR":"WE DONT HAVE THIS USERNAME"})
    else:
        ser=UserSerializers(user)
        return Response(ser.data)



@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,IsOwner))
def EditProfileView(request):
    user = User.objects.get(username=request.query_params['username'])

    if request.method=='PUT':
        ser=UserSerializers(user,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response({"ERROR":"DATA NOT VALID"})

    elif request.method=='GET':
        ser=UserSerializers(user)
        return Response(ser.data)







"""
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def AddBasketView(request):
    all_model=['Cellphone','Laptop','Tablet','Television']
    try:
            MODEL=request.data['model']

    except:
        return Response({"ERROR":"MODEL DOESNT IN YOYR INPUT"})
    else:
        if model in all_model:
            model=eval(MODEL)
            ser=Model_Json_Serializers(request.data)
            if ser.is_valid():
                obj=model.objects.get(pk=ser.data['id'])
                if (obj.stock-ser.data['number'])>=0:
                    obj.stock=obj.stock-ser.data['number']



                pass
            else:
                pass


        else:
            return Response({"ERROR":"YOUR MODEL DOESNT EXIST IN THIS PROJ"})
            """











