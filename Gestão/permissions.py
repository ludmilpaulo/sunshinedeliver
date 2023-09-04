from rest_framework.permissions import BasePermission



class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_customer)


class IsDriverUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_driver)