from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from post.models import Post
from .models import Like
from .serializers import LikeSerializer

class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({
                'status': 'liked', 
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'name': request.user.name,
                }
            }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({
                'status': 'unliked', 
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'name': request.user.name,
                }
            }, status=status.HTTP_204_NO_CONTENT)


class PostLikesList(generics.GenericAPIView):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'post_id': post.id,
            'liked_users': serializer.data
        }, status=status.HTTP_200_OK)