from django.db import models
from django.utils import timezone

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
        related_name="driver_profile",
    )

    # Driver Identity
    license_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )

    # Documents
    profile_photo = models.ImageField(
        upload_to="drivers/profile/",
        blank=True,
        null=True,
    )

    drivers_license_image = models.ImageField(
        upload_to="drivers/license/",
        blank=True,
        null=True,
    )

    national_id_image = models.ImageField(
        upload_to="drivers/national_id/",
        blank=True,
        null=True,
    )

    insurance_document = models.FileField(
        upload_to="drivers/insurance/",
        blank=True,
        null=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.OFFLINE,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
    )

    completed_deliveries = models.PositiveIntegerField(
        default=0,
    )

    current_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    current_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    last_location_update = models.DateTimeField(
        blank=True,
        null=True,
    )

    def update_location(self, latitude, longitude):
        self.current_latitude = latitude
        self.current_longitude = longitude
        self.last_location_update = timezone.now()

        self.save(
            update_fields=[
                "current_latitude",
                "current_longitude",
                "last_location_update",
            ]
        )

    @property
    def is_online(self):
        return self.availability_status == self.AvailabilityStatus.ONLINE

    @property
    def is_verified(self):
        return (
            self.verification_status == self.VerificationStatus.APPROVED
        )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"