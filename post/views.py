from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer


class CreatePost(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(cache_page(60 * 30, key_prefix="list_posts"), name="dispatch")
class ListPost(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        cache_key = f'user_{user_id}_posts'
        posts = cache.get(cache_key)

        if not posts:
            queryset = Post.objects.filter(user__id=str(user_id)).prefetch_related('comments')
            posts = list(queryset)
            cache.set(cache_key, posts, timeout=60 * 15)
        
        return posts


class UpdatePost(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'


class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
