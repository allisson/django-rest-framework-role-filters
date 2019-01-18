import json
import warnings

import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_get_allowed_actions(
        post1, post2, user_with_admin_role, user_with_user_role,
        client_admin_logged, client_user_logged):
    response = client_admin_logged.delete(reverse('testapp:posts-detail', args=[post1.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client_user_logged.delete(reverse('testapp:posts-detail', args=[post2.id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {'detail': 'action=destroy not allowed for role=user'}


def test_get_allowed_actions_with_no_declared_role_inside_view(
        post1, user_with_no_declared_role_in_view, client_user_logged):
    response = client_user_logged.delete(reverse('testapp:posts-detail', args=[post1.id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {'detail': 'action=destroy not allowed for role=no_post_access'}


def test_get_allowed_actions_with_obj_level_role_inside_view(
        post3, user_with_obj_level_role_in_view, client_user_logged):
    url = reverse('testapp:posts-detail', args=[post3.id])
    json_c_t = 'application/json'

    response = client_user_logged.get(url)
    assert response.status_code == status.HTTP_200_OK

    response = client_user_logged.put(
        url,
        data={'title': 'new', 'body': 'new_body'},
        content_type=json_c_t,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {'detail': 'action=update not allowed for role=obj_level_user'}

    response = client_user_logged.patch(
        url,
        data=json.dumps({'title': 'new title'}),
        content_type=json_c_t,
    )
    assert response.status_code == status.HTTP_200_OK

    response = client_user_logged.get(reverse('testapp:posts-list'))
    assert response.status_code == status.HTTP_200_OK


def test_deprecated_get_allowed_actions(
        post4, user_with_deprecated_role_in_view, client_user_logged):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        response = client_user_logged.delete(reverse('testapp:posts-detail', args=[post4.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {'detail': 'action=destroy not allowed for role=deprecated_user'}

        assert len(w) >= 1
        assert issubclass(w[-1].category, PendingDeprecationWarning)
        msg = str(w[-1].message)
        assert "deprecated" in msg
        assert "`obj` argument" in msg



def test_get_queryset(
        post1, post2, user_with_admin_role, user_with_user_role,
        client_admin_logged, client_user_logged):
    url = reverse('testapp:posts-list')

    response = client_admin_logged.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2

    response = client_user_logged.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_get_serializer_class(
        post1, post2, user_with_admin_role, user_with_user_role,
        client_admin_logged, client_user_logged):
    url = reverse('testapp:posts-list')

    response = client_admin_logged.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['serializer_name'] == 'PostSerializer'

    response = client_user_logged.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['serializer_name'] == 'PostSerializerForUser'


def test_get_serializer(
        post1, post2, user_with_admin_role, user_with_user_role,
        client_admin_logged, client_user_logged):
    url = reverse('testapp:posts-list')

    response = client_admin_logged.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'admin_only_field' in response.data['results'][0]

    response = client_user_logged.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'admin_only_field' not in response.data['results'][0]
