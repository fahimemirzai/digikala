from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from app_product.models import Cellphone



class IsOwner(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            user=User.objects.get(username=request.query_params['username'])
        except:
            return False

        if request.user.is_superuser or request.user==user:
            return True

        else:
            return False




class MustAnonymouse(permissions.BasePermission):
    def has_permission(self,request,view):
        #import ipdb ; ipdb.set_trace()
        if request.user.is_anonymous:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False

#
# class OneComment(permissions.BasePermission):
#     def has_permission(self,request,view):
#         pass

class Comment_Owner(permissions.BasePermission):#برای قسمت های دیلیت و اپدیت

    def has_permission(self,request,view):

        # id=view.kwargs.get('pk', None)#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        try:
            obj_id=request.GET["obj_id"]
            obj_type=request.GET["obj_type"]
            ct=ContentType.objects.get(model=obj_type.lower())
            comment=Comment.objects.get(user=request.user,content_type=ct,object_id=int(obj_id))
        except:
            return False

        return True


class PublishPermission(permissions.BasePermission):#فقط برای قسمت اپدیت یک کامنتا
    def has_permission(self,request,view):

        try:
            obj_id = request.GET["obj_id"]
            obj_type = request.GET["obj_type"]
            ct = ContentType.objects.get(model=obj_type.lower())
            comment = Comment.objects.get(user=request.user, content_type=ct, object_id=int(obj_id))
        except:
            return False

        # import ipdb; ipdb.set_trace()
        if comment.publish==True:
            return False
        else:
            return True





class JustOneComment(permissions.BasePermission):

    def has_permission(self,request,view):
        MODELS = ['Cellphone', 'Tablet', 'Laptop', 'Television']
        # import ipdb; ipdb.set_trace()
        if request.GET.get("obj_id") and request.GET.get("obj_type") and  request.GET.get("obj_type") in MODELS:
            obj_id = request.GET["obj_id"]
            obj_type = request.GET["obj_type"]
            mdl=eval(obj_type)
        else:
            return False

        try:
            ct = ContentType.objects.get(model=obj_type.lower())
            product = mdl.objects.get(pk=int(obj_id))
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
            # import ipdb; ipdb.set_trace()
            id=request.GET["id"]
            id=int(id)
            comment = Comment.objects.get(pk=id)
        except:
            return False

        if comment.user==request.user:
            return False
        else:
            return True




