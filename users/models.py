from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Profile(models.Model):
    """ Profile Model
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    website = models.URLField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.username

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.email + self.username