from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'last_request']