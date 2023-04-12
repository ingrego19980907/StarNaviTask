from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, PostLike
from .serializers import LikePostSerializer, PostSerializer


class CreatePostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeView(generics.GenericAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        post_like, created = PostLike.objects.get_or_create(user=user, post=post)
        post.likes_count += 1
        post.save()
        serializer = self.get_serializer(post_like)
        return Response(serializer.data)


class PostUnlikeView(generics.GenericAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        post_like = PostLike.objects.filter(user=user, post=post).first()
        if post_like:
            post_like.delete()
            post.likes_count -= 1
            post.save()
        serializer = self.get_serializer(post_like)
        return Response(serializer.data)
