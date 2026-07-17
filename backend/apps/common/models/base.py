from .audit import AuditModel
from .soft_delete import SoftDeleteModel
from .timestamped import TimeStampedModel
from .uuid_model import UUIDModel


class BaseModel(
    TimeStampedModel,
    UUIDModel,
    SoftDeleteModel,
    AuditModel,
):
    """
    Base model inherited by all CargoFlow models.
    """

    class Meta:
        abstract = True