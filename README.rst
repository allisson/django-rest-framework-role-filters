django-rest-framework-role-filters
==================================

.. image:: https://travis-ci.org/allisson/django-rest-framework-role-filters.svg?branch=master
    :target: https://travis-ci.org/allisson/django-rest-framework-role-filters

.. image:: https://codecov.io/gh/allisson/django-rest-framework-role-filters/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/allisson/django-rest-framework-role-filters

How to install
--------------

.. code:: shell

    pip install djangorestframework-role-filters

How to use
----------

Create role_filters.py with your roles definitions

.. code:: python
    
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

Create viewset and override get_role_id method

.. code:: python
    
    from rest_framework_role_filters.role_filters import RoleFilterGroup
    from rest_framework_role_filters.viewsets import RoleFilterModelViewSet

    from .models import Post
    from .role_filters import AdminRoleFilter, UserRoleFilter
    from .serializers import PostSerializer


    class PostViewSet(RoleFilterModelViewSet):
        role_filter_group = RoleFilterGroup(role_filters=[AdminRoleFilter(), UserRoleFilter()])
        queryset = Post.objects.all()
        serializer_class = PostSerializer

        def get_role_id(self, request):
            return request.user.role.role_id

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

If role_id is 'admin':

* All actions is allowed
* The default queryset is returned - Post.objects.all()
* The default serializer_class is used - PostSerializer

If role_id is 'user':

* Only actions 'create', 'list', 'retrieve', 'update', 'partial_update' is allowed
* The queryset is filtered by user
* The serializer_class PostSerializerForUser is used

Check `testapp example <https://github.com/allisson/django-rest-framework-role-filters/tree/master/testproject/testapp>`_ code implementation.
