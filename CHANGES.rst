Changelog
---------

1.0.1
~~~~~

* Create property role_filter_group on RoleFilterMixin to avoid error with get_schema_view.

1.0.0
~~~~~

* Replace RoleFilterMixin role_filter_group with role_filter_classes (thanks @hugobrilhante).
* Replace Travis with Github Actions.
* Drop Python 3.5 support.
* Drop DRF 3.5.x/3.6.x/3.7.x/3.8.x/3.9.x support.
* Add suport for DRF 3.10.x/3.11.x.
* Drop support for Django 1.11.x/2.0.x/2.1.x.
* Add support for Django 2.2.x/3.0.x. 
* Apply black format on project.
* Apply isort on project.

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
