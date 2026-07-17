from django.db import models
from apps.accounts.models.user import User
from apps.common.models import BaseModel

class DriverProfile(BaseModel):
    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        SUSPENDED = "SUSPENDED", "Suspended"

    class AvailabilityStatus(models.TextChoices):
        OFFLINE = "OFFLINE", "Offline"
        ONLINE = "ONLINE", "Online"
        BUSY = "BUSY", "Busy"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="driver_profile"
    )

    license_number = models.CharField(
        max_length=100,
        unique=True
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )

    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.OFFLINE
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00
    )

    completed_deliveries = models.PositiveIntegerField(
        default=0
    )

    current_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    current_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.email} Driver Profile"