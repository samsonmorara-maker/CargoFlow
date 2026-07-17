from django.db import models


class ActiveManager(models.Manager):
    """
    Returns only objects that have not been soft deleted.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    """
    Returns all objects, including soft deleted ones.
    """

    def get_queryset(self):
        return super().get_queryset()