import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    Abstract model that provides a UUID field.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    class Meta:
        abstract = True