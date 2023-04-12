from posts.models import Post
from django.urls import reverse

def test_login(api_client, user):
    url = reverse("login")
    data = {
        "email": user.email,
        "password": "password"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()


def test_create_post(api_client, user):
    url = reverse("create_post")
    api_client.force_authenticate(user=user)
    data = {
        "title": "Test post",
        "body": "Test post body"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert Post.objects.filter(title="Test post", body="Test post body").exists()


def test_like_post(api_client, user, post):
    url = reverse("post_like", args=[post.pk])
    api_client.force_authenticate(user=user)
    response = api_client.post(url)
    assert response.status_code == 200
    assert post.likes_count == 0

def test_unlike_post(api_client, user, post):
    url = reverse("post_unlike", args=[post.pk])
    api_client.force_authenticate(user=user)
    response = api_client.post(url)
    assert response.status_code == 200
    assert post.likes.count() == 0


def test_user_activity(api_client, user):
    url = reverse("user_activity")
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert "last_login" in response.json()
    assert "last_request" in response.json()


def test_post_analytics(api_client, user, post):
    date_from = "2023-02-02"
    date_to = "2023-07-15"
    url = f"/api/analytics/like_count_by_date/?date_from={date_from}&date_to={date_to}"
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
