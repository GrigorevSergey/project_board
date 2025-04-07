from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsProjectMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsBoardAssign(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        return request.user in obj.assign.all()
