from django.db import models
from django.utils.text import slugify
from django.conf import settings
from ckeditor.fields import RichTextField
from .managers import PostsManager

# Create your models here.


class Category(models.Model):
    """Category model"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """Post model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, unique=True)
    image_header = models.ImageField(upload_to='posts/photos')
    post = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category)

    objects = PostsManager()

    def __str__(self) -> str:
        return f" Author: {self.user.username} Title: {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Comment(models.Model):
    """Comment class"""

    # user = models.ForeignKey(User, on_delete=models.PROTECT)
    # profile = models.ForeignKey('users.Profile', on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    comment = models.CharField(max_length=5000)

    def __str__(self) -> str:
        return self.comment
