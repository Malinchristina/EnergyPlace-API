from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    """
    Post model, references User model as owner.
    Default image is set to a placeholder image.
    References Location and Category models.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='images/', default='../default_post_lskfrc', blank=True #remove blank=True after testing
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # location = models.ForeignKey(
    #     'Location', on_delete=models.SET_NULL, null=True, blank=True
    # )
    # category = models.ForeignKey(
    #     'Category', on_delete=models.SET_NULL, null=True, blank=True
    # )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
