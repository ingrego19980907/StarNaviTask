import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from users.models import EmailRequiredUser as User
from posts.models import Post

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password'
    )

@pytest.fixture
def post(user):
    return Post.objects.create(
        title='Test post',
        body='Test post body',
        author=user
    )