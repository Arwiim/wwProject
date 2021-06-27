from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    """ Profile Model
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    website = models.URLField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    coderegistro = models.CharField(max_length=12, default='000000000000')
    
    def __str__(self) -> str:
        return self.user.username