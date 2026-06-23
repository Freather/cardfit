from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    PopularPostListView,
    CommentListCreateView,
    CommentDetailView,
    PostLikeView,
    PostViewView,
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/popular/', PopularPostListView.as_view(), name='post-popular'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:pk>/comments/<int:comment_pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('posts/<int:pk>/view/', PostViewView.as_view(), name='post-view'),
]
