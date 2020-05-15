from django.urls import path
from . import views

app_name = 'app_product'
urlpatterns = [
    #path('', views.base, name='base'),
    #path('all-cellphone/', views.AllCellphone.as_view(), name='all-cellphone'),
    # path('all-cellphone/<int:pk>/', views.Cellphone.as_view(), name='cellphone'),
    path('product-list/',views.ProductList.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),

]