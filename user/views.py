from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import generics, permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from post.serializers import PostSerializer
from post.models import Post

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDelete(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_follow.followers.filter(id=request.user.id).exists():
            return Response({'detail': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        user_to_follow.followers.add(request.user)
        return Response({'detail': 'Successfully followed the user'}, status=status.HTTP_200_OK)


class UnfollowUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({'error': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if not user_to_unfollow.followers.filter(id=request.user.id).exists():
            return Response({'detail': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)

        user_to_unfollow.followers.remove(request.user)
        return Response({'detail': 'Successfully unfollowed the user'}, status=status.HTTP_200_OK)


class FollowersList(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        followers = user.followers.all()
        follower_data = [{'id': follower.id, 'username': follower.username} for follower in followers]

        return Response({'followers': follower_data}, status=status.HTTP_200_OK)


class FollowingList(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        following = user.following.all()
        following_data = [{'id': follow.id, 'username': follow.username} for follow in following]

        return Response({'following': following_data}, status=status.HTTP_200_OK)
    

@method_decorator(cache_page(15 * 1, key_prefix="user_timeline"), name="dispatch")
class TimelineView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        cache_key = f'user_timeline_{user_id}'
        posts = cache.get(cache_key)

        if not posts:   
            user = User.objects.get(id=user_id)
            following_ids = user.following.values_list('id', flat=True)
            user_and_following_ids = list(following_ids) + [user.id]

            queryset = Post.objects.filter(user__id__in=user_and_following_ids).order_by('-created_at')
            posts = list(queryset)
            cache.set(cache_key, posts, timeout=15 * 1)
        
        return posts

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)