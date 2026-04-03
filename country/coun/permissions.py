from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "Only owners can create restaurants"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "owner"
    
    
class IsCustomer(BasePermission):
    message = "Only customers allowed"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"
    
class IsRestaurantOwner(BasePermission):
    message = "Not your restaurant"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsFoodOwner(BasePermission):
    message = "Not your restaurant food"

    def has_object_permission(self, request, view, obj):
        return obj.restaurant.owner == request.user