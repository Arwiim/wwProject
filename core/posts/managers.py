from django.db import models


class PostsManager(models.Manager):
    """Manager for Posts"""

    def list_books(self, kword):

        res = self.filter(
            title__icontains=kword,
        )

        return res
