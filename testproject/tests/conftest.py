from __future__ import absolute_import
import pytest
from rest_framework.test import APIClient

from testapp.models import UserRole, Post


@pytest.fixture
def user_with_admin_role(django_user_model):
    user = django_user_model.objects.create_user('admin', 'admin@email.com', '123456')
    UserRole.objects.create(user=user, role_id='admin')
    return user


@pytest.fixture
def user_with_user_role(django_user_model):
    user = django_user_model.objects.create_user('user', 'user@email.com', '123456')
    UserRole.objects.create(user=user, role_id='user')
    return user


@pytest.fixture
def user_with_no_declared_role_in_view(django_user_model):
    user = django_user_model.objects.create_user('user', 'user@email.com', '123456')
    UserRole.objects.create(user=user, role_id='no_post_access')
    return user


@pytest.fixture
def client_admin_logged(client):
    client = APIClient()
    client.login(username='admin', password='123456')
    return client


@pytest.fixture
def client_user_logged(client):
    client = APIClient()
    client.login(username='user', password='123456')
    return client


@pytest.fixture
def post1(user_with_admin_role):
    return Post.objects.create(
        user=user_with_admin_role,
        title='My Post Title',
        body='My Post Body'
    )


@pytest.fixture
def post2(user_with_user_role):
    return Post.objects.create(
        user=user_with_user_role,
        title='My Post Title',
        body='My Post Body'
    )
