from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "You are not the owner of this email"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
