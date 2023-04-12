from django.urls import path

from .views import LikeAnalyticsView
from .views import UserActivityView


urlpatterns = [
    path(r'like_count_by_date/', LikeAnalyticsView.as_view(), name="like_count_by_date"),
    path(r'user_activity/', UserActivityView.as_view(), name="user_activity"),
]
