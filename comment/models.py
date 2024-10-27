import uuid
from django.db import models


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
