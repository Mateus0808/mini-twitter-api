from django.urls import path
from .views import CreatePost, ListPost, UpdatePost, DeletePost


urlpatterns = [
    path('create/', CreatePost.as_view(), name='create-post'),
    path('by-user/<uuid:user_id>/', ListPost.as_view(), name='list-posts-by-user'),
    path('update/<uuid:id>/', UpdatePost.as_view(), name='update-post'),
    path('delete/<uuid:id>/', DeletePost.as_view(), name='delete-post'),
]