from django.conf import settings
from django.db import models


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('general', '일반'),
        ('review', '카드 후기'),
        ('question', '질문'),
        ('info', '정보'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='general', verbose_name='카테고리'
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'community_post'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'community_comment'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.post.title} - {self.user.email}'

    @property
    def likes_count(self):
        return self.likes.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_postlike'
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_post_like'),
        ]


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_commentlike'
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name='unique_comment_like'),
        ]
