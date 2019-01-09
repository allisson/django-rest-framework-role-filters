import warnings

__all__ = ['RoleFilterMixin']


class RoleFilterMixin(object):
    role_filter_group = None
    role_id = None

    def get_role_id(self, request):
        pass

    def initial(self, request, *args, **kwargs):
        super(RoleFilterMixin, self).initial(request, *args, **kwargs)
        self.role_id = self.get_role_id(request)
        allowed_actions = self.role_filter_group.get_allowed_actions(self.role_id, request, self)
        if self.action not in allowed_actions:
            self.permission_denied(
                request,
                message='action={} not allowed for role={}'.format(self.action, self.role_id)
            )

    def get_queryset(self):
        queryset = super(RoleFilterMixin, self).get_queryset()
        filtered_queryset = self.role_filter_group.get_queryset(self.role_id, self.request, self, queryset)
        if filtered_queryset is None:
            return queryset
        return filtered_queryset

    def get_serializer_class(self):
        serializer_class = super(RoleFilterMixin, self).get_serializer_class()
        filtered_serializer_class = self.role_filter_group.get_serializer_class(
            self.role_id, self.request, self
        )
        if filtered_serializer_class is None:
            return serializer_class
        return filtered_serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        filtered_serializer = self.role_filter_group.get_serializer(
            self.role_id, self.request, self, serializer_class, *args, **kwargs
        )
        if filtered_serializer is None:
            return serializer_class(*args, **kwargs)
        return filtered_serializer

    def check_object_permissions(self, request, obj):
        super(RoleFilterMixin, self).check_object_permissions(request, obj)

        allowed_actions = self.role_filter_group.get_allowed_actions(self.role_id, request, self, obj=obj)
        if self.action not in allowed_actions:
            self.permission_denied(
                request,
                message='action={} not allowed for role={}'.format(self.action, self.role_id)
            )
