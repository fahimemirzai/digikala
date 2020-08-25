from django_graphene_permissions.permissions import BasePermission




class IsOwner(BasePermission):

    @staticmethod
    def has_permission(context,):
        import ipdb; ipdb.set_trace()
        return True





