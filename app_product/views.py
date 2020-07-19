from django.shortcuts import render
# from django.views import generic
from .models import Cellphone,Television
from .serializer import CellphoneSerializer,SearchSerializer,AllCellphoneSerializer,ErrorSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from itertools import chain
from django_filters.rest_framework import DjangoFilterBackend



class ProductList(generics.ListAPIView):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ##queryset = Cellphone.objects.all()
    ##serializer_class = CellphoneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','stock','price']

    def get_queryset(self):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        product_type = self.request.GET.get('type')#@@@@@@@@@@@@@@@@@@@@@@@@@ self=یادته هر وقت یک تابع داخل یک کلاس بود
        if product_type in MODELS:
            product_model = eval(product_type)
            return product_model.objects.all()
        else:
            return Cellphone.objects.none()


    def get_serializer_class(self):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        product_type = self.request.GET.get('type')
        if product_type == 'Cellphone':
            return AllCellphoneSerializer
        elif product_type == 'Tablet':
            pass #سریالایزر مربوط بهش که الان ندارم
        elif product_type == 'Laptop':
            pass
        elif product_type == 'Television':
            pass
        else:
            return ErrorSerializer


class ProductDetail(generics.RetrieveAPIView):
    #queryset = Cellphone.objects.all()
    #serializer_class = CellphoneSerializer
    lookup_field='pk'
    def get_queryset(self):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        product_type = self.request.GET.get('type')
        if product_type in MODELS:
            product_model = eval(product_type)
            return product_model.objects.all()
        else:
            return Cellphone.objects.none()

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
            return ErrorSerializer






class Search(generics.ListAPIView):# همش @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    serializer_class=SearchSerializer
    def get_queryset(self):
        query=self.request.GET.get('q',None)

        if query is not None:
            cellphone_results = Cellphone.sm.search(query)###############مخصوصا این قسمت-خروجی یک کویری ست هست
            television_results = Television.sm.search(query)

            queryset_chain = chain(
                cellphone_results,
                television_results

            )
            # import ipdb; ipdb.set_trace()

            # qs = sorted(queryset_chain,
            #             key=lambda instance: instance.pk,
            #             reverse=True)
            # # self.count = len(qs)
            qs=queryset_chain# اینو بعدا نوشتم چون بالایی رو کامنت کردم چون نمیدونستم چی کار می کنه اگر مشکل بالایی حل شد اینو حذف کن
            return qs

        return Cellphone.sm.none()#یک کویری ست خالی برمی گردونه


#
# @api_view(['GET'])
# def image(request):
#     album=Album.objects.all()
#     ser=AlbumSerializer(album,many=True)
#     return Response(ser.data)
