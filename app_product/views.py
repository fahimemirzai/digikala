from django.shortcuts import render
from django.views import generic
from .models import Cellphone
from .serializer import CellphoneSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


class AllCellphone(generics.ListAPIView):
    queryset = Cellphone.objects.all()
    serializer_class = CellphoneSerializer


class CellphoneDetail(generics.RetrieveAPIView):
    queryset = Cellphone.objects.all()
    serializer_class = CellphoneSerializer
    






