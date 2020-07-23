from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Comment,Basket,ReturningBasket,BasketItem,Address
from django.contrib.contenttypes.models import ContentType
from app_product.models import Cellphone
import datetime




class ActiveTrueBasket(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            pk=view.kwargs.get('pk') #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            basket = Basket.objects.filter(user=request.user, pk=pk ).exclude(status='favorites').exclude(status='canceled')
            basket=basket.first()
            if bool(basket)==False:
                return False

        except:
            return False

        if basket.basketitem_set.all().count() == 0:
            return False

        if basket.deliverydate==None:
            return True
        elif (basket.deliverydate.date-datetime.date.today()).days <=1:
            return False
        else:
            return True





class IsOwner(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            address=Address.objects.get(pk=view.kwargs['pk'])
        except:
            return False
        # if request.user.is_superuser or request.user==user:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if address.profile.user==request.user :#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ address__profile__user به این شکل اشتباهه حواست باشه
            return True
        else:
            return False




class MustAnonymouse(permissions.BasePermission):
    def has_permission(self,request,view):

        if request.user.is_anonymous or request.user.is_superuser:#@@@@@@@@@@@@@@@@@@@@@
            return True
        else:
            return False

#
# class OneComment(permissions.BasePermission):
#     def has_permission(self,request,view):
#         pass

class Comment_Owner(permissions.BasePermission):#برای قسمت های دیلیت و اپدیت
    def has_permission(self,request,view):

        pk=view.kwargs.get('pk',None) #@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        try:
            comment=Comment.objects.get(pk=pk,user=request.user)
            return True
        except:
            return False



class PublishPermission(permissions.BasePermission):#فقط برای قسمت اپدیت یک کامنتا

    def has_permission(self,request,view):
        try:

            # obj_id = request.GET["obj_id"]
            # obj_type = request.GET["obj_type"]
            # ct = ContentType.objects.get(model=obj_type.lower())
            # comment = Comment.objects.get(user=request.user, content_type=ct, object_id=int(obj_id),
            #                               pk=view.kwargs['pk'])
            comment=Comment.objects.get(pk=view.kwargs['pk'])

        except:
            print("*" *100)
            return False

        if comment.publish==True:
            print("!"*100)
            return False
        else:
            return True



class JustOneComment(permissions.BasePermission):

    def has_permission(self,request,view):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        try:
            obj_id = request.GET["obj_id"]
            obj_type = request.GET["obj_type"]

            mdl=eval(obj_type) #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@==<class 'app_product.models.Cellphone'>
            product = mdl.objects.get(pk=int(obj_id))
            ct = ContentType.objects.get(model=obj_type.lower())# @@@@@@@@@@@@@@@@@@@@@@@==<ContentType: cellphone>

        except:
            return False

        try:
            comment = Comment.objects.get(user=request.user, content_type=ct, object_id=int(obj_id))
        except:
           return True
        return False



class IsNotOwner(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            pk=view.kwargs['pk']
            comment = Comment.objects.get(pk=pk)
        except:
            return False

        if comment.user==request.user:
            return False
        else:
            return True






class AdressRegisterAbility(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            order=request.GET['order']
        except:
            return False

        if  order=='buy':
            try:
              pk=view.kwargs.get('pk')
              basket=Basket.objects.filter(pk=pk,user=request.user).exclude(status='favorites').\
                  exclude(status='delivered').exclude(status='canceled') #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              basket=basket.first() #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              if bool(basket)==False:
                  return False
              if basket.address==None :
                  return True
              elif (basket.deliverydate.date - datetime.date.today()).days >=1:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-->days
                  return True
              else:
                  return False

            except:
                return False

        elif order=='returned':
            try:
                pk = view.kwargs.get('pk')
                return_basket=ReturningBasket.objects.get(pk=pk,user=request.user,status='accepted')

                if return_basket.address==None:
                    return True
                elif (return_basket.returning_date.returning_date - datetime.date.today()).days >= 1: #@@@@@@@@@@@@@@@@@@@@@
                    return True
                else:
                    return False
            except:

                return False
        else:
            return False




class ReturnTimeLimit(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            basket=Basket.objects.get(pk=view.kwargs.get('pk'),user=request.user)
            return_time_range = [basket.deliverydate.date + datetime.timedelta(i) for i in range(0, 7)]
            now = datetime.date.today()
        except:
            return False

        if (now in return_time_range) and (basket.delivered==True) :
            return True
        else:
            return False

class HaveInactiveReturningBasket(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            pk=view.kwargs['pk']
            basket=Basket.objects.get(pk=pk)
            return_basket=basket.returningbasket_set.filter(basket=basket).exclude(status='canceled').\
                exclude(status='received')
        except:
            return False
        if bool(return_basket)==True:
            return False
        else:
            return True


class HaveActiveReturningBasket(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            pk = view.kwargs['pk']
            basket = Basket.objects.get(pk=pk)
            return_basket = basket.returningbasket_set.filter(basket=basket).exclude(status='canceled').\
                exclude(status='received')
            return_basket=return_basket.first()
        except:
            return False


        now=datetime.date.today()
        return_date=return_basket.returning_date
        if bool(return_basket.returning_date):
            days=(return_basket.returning_date.returning_date - now).days
            if bool(return_basket) == True and days>0 :
                return True
            else:
                return False

        else:
            return True




class AllowedToSet(permissions.BasePermission):
    def has_permission(self,request,view):

        return_basket=ReturningBasket.objects.filter(pk=view.kwargs.get('pk'),user=request.user).\
            exclude(status='canceled').exclude(status='received')
        # import ipdb; ipdb.set_trace()
        return_basket=return_basket.first()
        if bool(return_basket)==False:
            return False

        return_time_range=[return_basket.basket.deliverydate.date + datetime.timedelta(i) for i in range(0,7)]
        now=datetime.date.today()
        if not(now in return_time_range):
            return False


        if return_basket.returning_date :
            if (return_basket.returning_date.returning_date - datetime.date.today()).days >1:
                return True
            else:
                return False
        else:
            return True



class AllowCancelledReturnBasket(permissions.BasePermission):
    def has_permission(self,request,view):
        try:

            return_basket=ReturningBasket.objects.filter(pk=view.kwargs.get('pk'),user=request.user).exclude(status='canceled').\
                exclude(status='received')
            return_basket=return_basket.first()
            if not(return_basket):
                return False
        except:
            return False
        try:
            time_diffrence=(return_basket.returning_date.returning_date - datetime.date.today()).days
            if time_diffrence >0:#همون روز نمیشه پس مساوی صفر نداریم
                return True
            else:
                return False
        except:
            return True

class CancelledTimeLimit(permissions.BasePermission):#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def has_permission(self,request,view):
        try:
            # import ipdb;
            # ipdb.set_trace()
            basket=Basket.objects.get(pk=view.kwargs['pk'],user=request.user,status='pardakht-shod')
        except:
            return False

        try:

            if bool(basket.deliverydate)==False:
                return True
            ln=( basket.deliverydate.date - basket.order_registration_date ).days
            date_range=[basket.order_registration_date + datetime.timedelta(i) for i in range(0,ln)]
            now=datetime.date.today()
        except:
            return False
        if (now in date_range) and (basket.delivered==False):
            return True
        else:
            return False



class YourOrder(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            order = Basket.objects.get(pk=view.kwargs['pk'], user=request.user)
        except:
            return False
        return True

class YourReturnBasket(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            pk=view.kwargs['pk']
            return_basket=ReturningBasket.objects.get(pk=pk,user=request.user)
        except:
            return False
