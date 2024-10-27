from django.urls import path
from .views import LikeToggleView, PostLikesList

urlpatterns = [
    path('like-toggle/', LikeToggleView.as_view(), name = 'toggle-like'),
    path('post-like-list/<uuid:post_id>/', PostLikesList.as_view(), name = 'post-like-list')
]