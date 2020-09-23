from django.urls import path, include
from . import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    # -------------------------------------------------registeration & login(with username & password)---------------
    path('registration', views.register),

    path('api-token-auth', rest_views.obtain_auth_token),
    path('api-auth', include('rest_framework.urls')),

    path('change-password', views.change_password),
    # -------------------------------------------------registeration & login(with sms)---------------------------
    path('login-register/', views.login_register),
    path('confirm-code/', views.confirm_code),
    # -----------------------------------------------------------------------------------------------------------
    path('show-addresses', views.show_address),
    path('add-address', views.add_address),
    path('edite-address/<int:pk>', views.edit_address),
    path('delete-address/<int:pk>', views.delete_address),

    path('show-basket', views.show_basket),
    path('add-basket', views.add_basket_item),  # @@@@@@@@@@
    path('reduce-basket', views.reduce_basket_item),  # @@@@@@@@@@

    path('show-favorites', views.show_favorites),
    path('add-reduce-favorites', views.add_reduce_favorites),

    path('my-comments', views.my_comments),
    path('show-comment/', views.show_comment),  # $$$$$$$$$$$$
    path('comment/add/', views.add_comment),  # $$$$$$$$$$
    path('comment/update/<int:pk>/', views.update_comment),  # $$$$$$$$$$$$$$$?????
    path('comment/delete/<int:pk>', views.delete_comment),
    path('comment/like/<int:pk>', views.like_comment),

    path('my-orders/', views.show_orders),
    path('my-orders/<int:pk>', views.order_item),  # @@@@@@@@ ???



    # #################################################################################################

    path('profile', views.profile, name='profile'),
    path('profile/edit', views.edit_profile),



    path('show-returning-basket/<int:pk>/', views.show_returning_basket),
    path('add-delivery-address/<int:pk>', views.add_delivery_address),

    path('add-delivery-date/<int:pk>', views.add_delivery_date),
    path('cancel-item-or-basket/<int:pk>', views.cancel_item_or_basket),
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    path('returning-basket-canceled/<int:pk>', views.canceled_returning_basket),
    path('add-returning-date/<int:pk>', views.add_returning_date),
    path('add-returning-items/<int:pk>', views.add_returning_items),
    path('edite-returning-items/<int:pk>', views.edite_returning_items),


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # path('add-question/', views.add_question),
    # path('add-reply/', views.add_reply),
    # path('like-dislike-reply/', views.like_dislike_reply),
    # path('show-question_reply/', views.show_quesstion_reply),

]
