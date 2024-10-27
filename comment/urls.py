from django.urls import path
from .views import CreateComment, ListCommentsOnPost, UpdateComment, DeleteComment


urlpatterns = [
    path('create/<uuid:user_id>/', CreateComment.as_view(), name='create-comment'),
    path('<uuid:post_id>/', ListCommentsOnPost.as_view(), name='list-comments-on-post'),
    path('update/', UpdateComment.as_view(), name='update-comment'),
    path('delete/<uuid:id>/', DeleteComment.as_view(), name='delete-comment'),
]