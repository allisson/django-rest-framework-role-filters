import warnings

__all__ = ["RoleFilter", "RoleFilterGroup"]


class RoleFilter:
    role_id = None

    def trigger_filter(self, filter_name, *args, **kwargs):
        selected_filter = getattr(self, filter_name)
        return selected_filter(*args, **kwargs)

    def get_allowed_actions(self, request, view, obj=None):
        """Return container of allowed actions.

        Defaults to list of all ViewSet actions.

        By default RoleFilterMixin calls this method during `ViewSet.initialize` with `obj=None`,
        and during `ViewSet.check_object_permissions` with `obj=something`.

        Should NOT return `None`.

        """
        actions = getattr(view, "action_map", {}) or {}
        actions = list(actions.values())
        actions = actions or ["create", "list", "retrieve", "update", "partial_update", "destroy"]
        return actions

    def get_queryset(self, request, view, queryset):
        """Return modified queryset for this role, or None if no modifications required."""
        return

    def get_serializer_class(self, request, view):
        """Return modified serializer class for this role, or None if no modifications required."""
        return

    def get_serializer(self, request, view, serializer_class, *args, **kwargs):
        """Return modified serializer instance for this role, or None if no modifications required."""
        return


class RoleFilterGroup:
    def __init__(self, role_filters):
        self.role_filters = {role_filter.role_id: role_filter for role_filter in role_filters}

    def get_role_filter(self, role_id):
        return self.role_filters.get(role_id)

    def trigger_filter(self, filter_name, role_id, *args, **kwargs):
        role_filter = self.get_role_filter(role_id)
        if role_filter is None:
            return
        return role_filter.trigger_filter(filter_name, *args, **kwargs)

    def get_allowed_actions(self, role_id, request, view, obj=None):
        try:
            allowed_actions = self.trigger_filter("get_allowed_actions", role_id, request, view, obj=obj)
        except TypeError:
            allowed_actions = self.trigger_filter("get_allowed_actions", role_id, request, view)
            warnings.warn(
                "RoleFilter.get_allowed_actions without support for `obj` argument is deprecated",
                PendingDeprecationWarning,
            )

        if allowed_actions is None:
            return []
        return allowed_actions

    def get_queryset(self, role_id, request, view, queryset):
        return self.trigger_filter("get_queryset", role_id, request, view, queryset)

    def get_serializer_class(self, role_id, request, view):
        return self.trigger_filter("get_serializer_class", role_id, request, view)

    def get_serializer(self, role_id, request, view, serializer_class, *args, **kwargs):
        return self.trigger_filter(
            "get_serializer", role_id, request, view, serializer_class, *args, **kwargs
        )
