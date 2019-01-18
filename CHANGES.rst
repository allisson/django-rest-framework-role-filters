Changelog
---------

0.3.0
~~~~~

* Using mixin approach for RoleFilterModelViewSet: code moved to RoleFilterMixin.
* get_allowed_actions now also accepts :code:`obj` argument that is used to verify actions
  allowed during :code:`check_object_permissions`.
* Drop python27 support.

0.2.3
~~~~~

* Add role_id to RoleFilterModelViewSet (fix drf docs pages).

0.2.2
~~~~~

* Handle not declared role inside a view.

0.2.1
~~~~~

* Update RoleFilterModelViewSet to check returned value from role filter (Fixes #1).

0.2.0
~~~~~

* Add get_serializer method to RoleFilter.

0.1.0
~~~~~

* Initial release.
