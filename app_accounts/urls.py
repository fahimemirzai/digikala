from django.urls import path, include

from . import views
from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('api-token-auth', rest_views.obtain_auth_token),
    path('api-auth', include('rest_framework.urls')),

    path('registration',views.register),
    path('ProfileView',views.ProfileView),
    path('EditProfileView', views.EditProfileView),


    path('show-basket',views.show_basket_item),
    path('add-basket',views.add_basket_item),
    path('reduce-basket',views.reduce_basket_item),

]
