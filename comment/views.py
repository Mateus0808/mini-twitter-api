from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer


class CreateComment(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        # Define o usuário autenticado como o autor do comentário
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        userLoggedId = str(self.request.user.id)

        if str(user_id) != userLoggedId:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_401_UNAUTHORIZED)

        return super().create(request, *args, **kwargs)
   

class ListCommentsOnPost(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post__id=str(post_id))

        return queryset


class UpdateComment(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'


class DeleteComment(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'