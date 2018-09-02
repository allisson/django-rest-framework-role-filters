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
