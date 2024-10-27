from django.urls import path
from .views import (
    UserCreate, 
    UserList, 
    UserDetail, 
    UserUpdate, 
    UserDelete, 
    FollowUser, 
    UnfollowUser,
    FollowersList,
    FollowingList,
    TimelineView
)


urlpatterns = [
    path('create/', UserCreate.as_view(), name = "create-user"),
    path('', UserList.as_view(), name = "list-user"),
    path('<uuid:id>/', UserDetail.as_view(), name = "user-detail"),
    path('update/<uuid:id>/', UserUpdate.as_view(), name = "update-user"),
    path('delete/<uuid:id>/', UserDelete.as_view(), name = "delete-user"),
    path('follow/<uuid:user_id>/', FollowUser.as_view(), name='follow-user'),
    path('follow-list/<uuid:user_id>/', FollowersList.as_view(), name='follow-user-list'),
    path('following-list/<uuid:user_id>/', FollowingList.as_view(), name='following-user-list'),
    path('unfollow/<uuid:user_id>/', UnfollowUser.as_view(), name='unfollow-user'),
    path('timeline/', TimelineView.as_view(), name='user-timeline'),
]