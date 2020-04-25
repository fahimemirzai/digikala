from django.urls import path, include

from . import views
from rest_framework.authtoken import views as rest_views


urlpatterns = [

    path('registration',views.RegisterView),
    path('ProfileView',views.ProfileView),
    path('EditProfileView', views.EditProfileView),

    path('api-token-auth', rest_views.obtain_auth_token),
    path('api-auth', include('rest_framework.urls')),

]
