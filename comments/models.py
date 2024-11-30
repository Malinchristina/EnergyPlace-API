from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.


class Comment(models.Model):
    """
    Comment model, references User and Post models.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.content}'
