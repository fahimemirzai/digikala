from django.shortcuts import render
from django.views import generic

from .models import Cellphone
from .serializer import CellphoneSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

"""
def base(request):
    return render(request, 'base.html')


class AllCellphone(generic.ListView):
    model = models.Cellphone
    template_name = 'app_product/all_cellphone.html'


class Cellphone(generic.DetailView):
    model = models.Cellphone
    template_name = 'app_product/cellphone.html'"""


class AllCellphoneListAPIView(generics.ListAPIView):
    queryset = Cellphone.objects.all()
    serializer_class = CellphoneSerializer


class CellphoneListAPIView(generics.RetrieveAPIView):
    queryset = Cellphone.objects.all()
    serializer_class = CellphoneSerializer

"""
@api_view(['POST'])
def BuyAPIView(request,pk):
      pass
"""
