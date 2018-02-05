from rest_framework.viewsets import ModelViewSet


class RoleFilterModelViewSet(ModelViewSet):
    role_filter_group = None

    def get_role_id(self, request):
        pass

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.role_id = self.get_role_id(request)
        allowed_actions = self.role_filter_group.get_allowed_actions(self.role_id, request, self)
        if self.action not in allowed_actions:
            self.permission_denied(
                request,
                message='action={} not allowed for role={}'.format(self.action, self.role_id)
            )

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.role_filter_group.get_queryset(self.role_id, self.request, self, queryset)
