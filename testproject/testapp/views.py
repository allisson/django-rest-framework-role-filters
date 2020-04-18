from rest_framework_role_filters.viewsets import RoleFilterModelViewSet

from .models import Post
from .role_filters import AdminRoleFilter, UserRoleFilter, ObjLevelUserRoleFilter, DeprecatedUserRoleFilter
from .serializers import PostSerializer


class PostViewSet(RoleFilterModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    role_filter_classes = [
        AdminRoleFilter,
        UserRoleFilter,
        ObjLevelUserRoleFilter,
        DeprecatedUserRoleFilter,
    ]

    def get_role_id(self, request):
        return request.user.role.role_id

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
