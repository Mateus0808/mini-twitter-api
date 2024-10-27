from rest_framework import serializers
from comment.serializers import CommentSerializer
from .models import Post
from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']