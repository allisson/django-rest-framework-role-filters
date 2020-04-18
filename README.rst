django-rest-framework-role-filters
==================================

.. image:: https://github.com/allisson/django-rest-framework-role-filters/workflows/tests/badge.svg
    :target: https://github.com/allisson/django-rest-framework-role-filters/actions

.. image:: https://img.shields.io/pypi/v/djangorestframework-role-filters.svg
        :target: https://pypi.python.org/pypi/djangorestframework-role-filters

.. image:: https://img.shields.io/github/license/allisson/django-rest-framework-role-filters.svg
        :target: https://pypi.python.org/pypi/djangorestframework-role-filters

.. image:: https://img.shields.io/pypi/pyversions/djangorestframework-role-filters.svg
        :target: https://pypi.python.org/pypi/djangorestframework-role-filters

How to install
--------------

.. code:: shell

    pip install djangorestframework-role-filters

Why i wrote this project?
-------------------------

I want work easily with roles without multiple ifs in code

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

        def get_allowed_actions(self, request, view, obj=None):
            # This example returns same list both for "global permissions" check,
            # and for "object" permissions, but different list may be returned
            # if `obj` argument is not None, and this list will be used to check
            # if action is allowed during call to `ViewSet.check_object_permissions`
            return ['create', 'list', 'retrieve', 'update', 'partial_update']

        def get_queryset(self, request, view, queryset):
            queryset = queryset.filter(user=request.user)
            return queryset

        def get_serializer_class(self, request, view):
            return PostSerializerForUser

        def get_serializer(self, request, view, serializer_class, *args, **kwargs):
            fields = (
                'body',
                'created_at',
                'id',
                'serializer_name',
                'title',
                'updated_at',
                'user',
            )
            return serializer_class(*args, fields=fields, **kwargs)

Create viewset and override get_role_id method

.. code:: python

    from rest_framework_role_filters.viewsets import RoleFilterModelViewSet

    from .models import Post
    from .role_filters import AdminRoleFilter, UserRoleFilter
    from .serializers import PostSerializer


    class PostViewSet(RoleFilterModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        role_filter_classes = [AdminRoleFilter, UserRoleFilter]

        def get_role_id(self, request):
            return request.user.role.role_id

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

If role_id is 'admin':

* All actions are allowed
* The default queryset is returned - :code:`Post.objects.all()`
* The default :code:`serializer_class` is used - :code:`PostSerializer`
* The default viewset :code:`get_serializer` method is used

If role_id is 'user':

* Only actions 'create', 'list', 'retrieve', 'update', 'partial_update' are allowed
* The queryset is filtered by user
* The :code:`serializer_class=PostSerializerForUser` is used
* The serializer initializing with :code:`fields` kwargs  (e.g. for modified serializer as described in
  `DRF: Dynamically modifying fields <https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields>`_)

Check `testapp example <https://github.com/allisson/django-rest-framework-role-filters/tree/master/testproject/testapp>`_ code implementation.
