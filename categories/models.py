from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.

class Category(models.Model):
    """
    Category model with predefined categories.
    """
    CATEGORY_CHOICES = [
        ('nature', 'Nature'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('cooking', 'Cooking'),
        ('other', 'Other'),
    ]

    name = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name
