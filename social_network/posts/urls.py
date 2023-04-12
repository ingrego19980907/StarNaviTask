from django.urls import path

from .views import CreatePostView
from .views import PostLikeView, PostUnlikeView


urlpatterns = [
    path(r'create/', CreatePostView.as_view(), name="create_post"),
    path(r'<int:pk>/like/', PostLikeView.as_view(), name="post_like"),
    path(r'<int:pk>/unlike/', PostUnlikeView.as_view(), name="post_unlike"),
]


