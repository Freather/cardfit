from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return CommentLike.objects.filter(comment=obj, user=request.user).exists()

    class Meta:
        model = Comment
        fields = (
            'id', 'user_email', 'username', 'content',
            'likes_count', 'is_liked', 'is_author',
            'created_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'user_email', 'username',
            'likes_count', 'is_liked', 'is_author',
            'created_at', 'updated_at',
        )


class PostListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return PostLike.objects.filter(post=obj, user=request.user).exists()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

    class Meta:
        model = Post
        fields = (
            'id', 'user_email', 'username', 'title', 'category',
            'views_count', 'likes_count', 'comments_count',
            'is_liked', 'is_author', 'created_at',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return PostLike.objects.filter(post=obj, user=request.user).exists()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

    class Meta:
        model = Post
        fields = (
            'id', 'user_email', 'username', 'title', 'content', 'category',
            'views_count', 'likes_count', 'comments_count',
            'comments', 'is_liked', 'is_author', 'created_at', 'updated_at',
        )
