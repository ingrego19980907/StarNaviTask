from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserActivitySerializer

from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import EmailRequiredUser as User
from posts.models import PostLike


class LikeAnalyticsView(APIView):
    def get(self, request, format=None):
        date_from_str = request.query_params.get("date_from")
        date_to_str = request.query_params.get("date_to")
        date_format = "%Y-%m-%d"

        try:
            date_from = datetime.strptime(date_from_str, date_format)
            date_to = datetime.strptime(date_to_str, date_format)
        except ValueError:
            return Response({"error": "Invalid date format. Use yyyy-mm-dd."}, status=status.HTTP_400_BAD_REQUEST)

        if date_to < date_from:
            return Response({"error": 'Invalid date range. "date_to" cannot be earlier than "date_from".'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = PostLike.objects.filter(created_at__range=(date_from, date_to))
        likes_by_day = {}
        for like in queryset:
            date_str = like.created_at.strftime(date_format)
            likes_by_day[date_str] = likes_by_day.get(date_str, 0) + 1

        data = [{"date": date, "likes": likes} for date, likes in likes_by_day.items()]
        return Response(data)


class UserActivityView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivitySerializer

    def get_object(self):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        return {
            'last_login': user.last_login,
            'last_request': user.last_request,
        }
