from django.urls import path, include

from . import views

urlpatterns = [

    path('registration',views.RegisterView),
    path('ProfileView',views.ProfileView),
    path('EditProfileView', views.EditProfileView),

]
