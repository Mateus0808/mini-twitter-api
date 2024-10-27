from django.db import models
from django.conf import settings
from post.models import Post


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_on_post')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Garante que um usuário só pode dar like uma vez por post

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'
