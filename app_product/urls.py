from django.urls import path
from . import views

app_name = 'app_product'
urlpatterns = [
    #path('', views.base, name='base'),
    #path('all-cellphone/', views.AllCellphone.as_view(), name='all-cellphone'),
    # path('all-cellphone/<int:pk>/', views.Cellphone.as_view(), name='cellphone'),
    path('all-cellphone/',views.AllCellphone.as_view(), name='all-cellphone'),
    path('all-cellphone/<int:pk>', views.CellphoneDetail.as_view(), name='cellphone_detail'),

]