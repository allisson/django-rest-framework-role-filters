from rest_framework_role_filters.role_filters import RoleFilter

from .serializers import PostSerializerForUser


class AdminRoleFilter(RoleFilter):
    role_id = "admin"


class UserRoleFilter(RoleFilter):
    role_id = "user"

    def get_allowed_actions(self, request, view, obj=None):
        return ["create", "list", "retrieve", "update", "partial_update"]

    def get_queryset(self, request, view, queryset):
        queryset = queryset.filter(user=request.user)
        return queryset

    def get_serializer_class(self, request, view):
        return PostSerializerForUser

    def get_serializer(self, request, view, serializer_class, *args, **kwargs):
        fields = (
            "body",
            "created_at",
            "id",
            "serializer_name",
            "title",
            "updated_at",
            "user",
        )
        return serializer_class(*args, fields=fields, **kwargs)


class ObjLevelUserRoleFilter(UserRoleFilter):
    role_id = "obj_level_user"

    def get_allowed_actions(self, request, view, obj=None):
        if obj is None:
            return ["create", "list", "retrieve", "update", "partial_update"]
        else:
            # This is strange but enough for tests. In real app you should probably check
            # user against some obj fields.
            return ["retrieve", "partial_update"]


class DeprecatedUserRoleFilter(UserRoleFilter):
    role_id = "deprecated_user"

    def get_allowed_actions(self, request, view):
        return ["create", "list", "retrieve", "update", "partial_update"]
