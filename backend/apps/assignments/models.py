from django.db import models
from apps.common.models import BaseModel
from apps.accounts.models import User
from apps.shipments.models import Shipment


class DriverAssignmentRequest(BaseModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        DECLINED = "DECLINED", "Declined"
        EXPIRED = "EXPIRED", "Expired"

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="assignment_requests",
    )

    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignment_requests",
        limit_choices_to={"role": User.Role.DRIVER},
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    offered_at = models.DateTimeField(
        auto_now_add=True,
    )

    responded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField()

    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    estimated_arrival_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    estimated_earnings = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["-offered_at"]

    def __str__(self):
        return f"{self.shipment.tracking_number} -> {self.driver.email}"