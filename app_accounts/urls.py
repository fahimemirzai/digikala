from django.urls import path, include
from . import views
from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('api-token-auth', rest_views.obtain_auth_token),
    path('api-auth', include('rest_framework.urls')),

    path('registration',views.register),
    path('change-password',views.change_password),


    #path('ProfileView',views.ProfileView),
    #path('EditProfileView', views.EditProfileView),
    path('profile', views.profile,name='profile'),
    path('profile/edit',views.edit_profile),

    path('show-addresses', views.address),
    path('address/<int:pk>', views.edit_address),
    path('add-address', views.add_address),



    path('show-basket',views.show_basket),
    path('add-basket',views.add_basket_item),
    path('reduce-basket',views.reduce_basket_item),

    path('favorites', views.favorite_basket),

    path('show-comment', views.show_comment),
    path('comment/delete/', views.delete_comment),
    # path('comment/update/', views.update_comment),

    path('comment/add/', views.add_comment),
    path('comment/like/', views.like_comment),

    path('my-orders/',views.show_orders),
    path('my-orders/<int:pk>', views.order_item),


]
