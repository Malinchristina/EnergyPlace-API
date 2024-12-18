from django.db import models
from django.contrib.auth.models import User
from locations.models import Location
from categories.models import Category


# Create your models here.

class Post(models.Model):
    """
    Post model, references User model as owner.
    Default image is set to a placeholder image.
    References Location and Category models and
    includes its own locality for specificity
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='images/',
        default='../default_post_lskfrc',
        blank=False
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    locality = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
