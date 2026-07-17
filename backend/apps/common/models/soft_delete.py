from django.db import models
from django.utils import timezone
from apps.common.managers import ActiveManager, AllObjectsManager

class SoftDeleteModel(models.Model):
    """
    Abstract model that enables soft deletion.
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    objects = ActiveManager()
    all_objects = AllObjectsManager()
    class Meta:
        abstract = True

    def soft_delete(self):
        """
        Marks the object as deleted instead of removing it
        from the database.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """
        Restores a previously soft-deleted object.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])