from rest_framework import permissions

from django.contrib.auth.models import User



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
        else:
            return False