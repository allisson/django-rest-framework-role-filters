from rest_framework.viewsets import ModelViewSet

from .mixins import RoleFilterMixin

__all__ = ["RoleFilterModelViewSet"]


class RoleFilterModelViewSet(RoleFilterMixin, ModelViewSet):
    pass
