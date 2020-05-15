from django.shortcuts import render
from django.views import generic
from .models import Cellphone
from .serializer import CellphoneSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ProductList(generics.ListAPIView):
    #queryset = Cellphone.objects.all()
    #serializer_class = CellphoneSerializer
    def get_queryset(self):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        product_type = self.request.GET.get('type')

        if product_type in MODELS:
            product_model = eval(product_type)
            return product_model.objects.all()
        else:
            return None

    def get_serializer_class(self):
        product_type = self.request.GET.get('type')
        if product_type == 'Cellphone':
            return CellphoneSerializer
        elif product_type == 'Tablet':
            pass #سریالایزر مربوط بهش که الان ندارم
        elif product_type == 'Laptop':
            pass
        elif product_type == 'Television':
            pass
        else:
            return None


class ProductDetail(generics.RetrieveAPIView):
    #queryset = Cellphone.objects.all()
    #serializer_class = CellphoneSerializer
    def get_queryset(self):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        product_type = self.request.GET.get('type')
        if product_type in MODELS:
            product_model = eval(product_type)
            return product_model.objects.all()
        else:
            return None

    def get_serializer_class(self):
        product_type = self.request.GET.get('type')
        if product_type == 'Cellphone':
            return CellphoneSerializer
        elif product_type == 'Tablet':
            pass  # سریالایزر مربوط بهش که الان ندارم
        elif product_type == 'Laptop':
            pass
        elif product_type == 'Television':
            pass
        else:
            return None

