from django.shortcuts import render
from django.views import generic

from . import models
from .serializer import AllcellphoneSerializer,CellphoneSerializer
from rest_framework import generics


def base(request):
    return render(request, 'base.html')


class AllCellphone(generic.ListView):
    model = models.Cellphone
    template_name = 'app_product/all_cellphone.html'


class Cellphone(generic.DetailView):
    model = models.Cellphone
    template_name = 'app_product/cellphone.html'


class AllCellphoneListAPIView(generics.ListAPIView):
    queryset = models.Cellphone.objects.all()
    serializer_class = AllcellphoneSerializer


class CellphoneListAPIView(generics.RetrieveAPIView):
    queryset = models.Cellphone.objects.all()
    serializer_class = CellphoneSerializer


