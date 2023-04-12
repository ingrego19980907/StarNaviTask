from rest_framework import serializers
from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "body", "created_at",
                  "updated_at", "author", "likes",
                  )

        read_only_fields = ("id", "created_at", "updated_at", "author", "likes",)


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ("user", "post", "created_at")
