from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
      def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE' and request.user and request.user.is_staff:
            return True
        return obj.owner == request.user