from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    topic = models.CharField(max_length=30)

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def get_absolute_url(self):
        return reverse('webprog:post',
                       args=[self.created.year,
                             self.created.month,
                             self.created.day,
                             self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


class MarkComment(models.Model):
    class Mark(models.TextChoices):
        LIKE = 'LK'
        DISLIKE = 'DK'

    mark = models.CharField(max_length=2,
                            choices=Mark.choices
                            )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='mark_comment')
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='user_mark_comment'
                                )


class MarkPost(models.Model):
    class Mark(models.TextChoices):
        LIKE = 'LK'
        DISLIKE = 'DK'

    mark = models.CharField(max_length=2,
                            choices=Mark.choices
                            )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='mark_post')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='user_mark_post'
                             )
