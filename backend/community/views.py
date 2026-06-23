from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Post, Comment, PostLike
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Post.objects.all()

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)

        search = request.query_params.get('search')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search))

        paginator = PostPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = PostListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostDetailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self._get_post(pk)
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = self._get_post(pk)
        if post.user != request.user:
            return Response({'detail': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostDetailSerializer(post, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        post = self._get_post(pk)
        if post.user != request.user:
            return Response({'detail': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PopularPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        posts_with_likes = sorted(posts, key=lambda p: (p.likes_count, p.views_count), reverse=True)[:10]
        serializer = PostListSerializer(posts_with_likes, many=True, context={'request': request})
        return Response(serializer.data)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(post.comments.all(), many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_comment(self, pk, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk, post_id=pk)

    def put(self, request, pk, comment_pk):
        comment = self._get_comment(pk, comment_pk)
        if comment.user != request.user:
            return Response({'detail': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, comment_pk):
        comment = self._get_comment(pk, comment_pk)
        if comment.user != request.user:
            return Response({'detail': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'liked': False, 'likes_count': post.likes_count})
        return Response({'liked': True, 'likes_count': post.likes_count})


class PostViewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Post.objects.filter(pk=pk).update(views_count=post.views_count + 1)
        return Response({'views_count': post.views_count + 1})
