from rest_framework_role_filters.role_filters import RoleFilter

from .serializers import PostSerializerForUser


class AdminRoleFilter(RoleFilter):
    role_id = 'admin'


class UserRoleFilter(RoleFilter):
    role_id = 'user'

    def get_allowed_actions(self, request, view):
        return ['create', 'list', 'retrieve', 'update', 'partial_update']

    def get_queryset(self, request, view, queryset):
        queryset = queryset.filter(user=request.user)
        return queryset

    def get_serializer_class(self, request, view):
        return PostSerializerForUser
