from django.db import models

from apps.common.models import BaseModel
from apps.shipments.models.shipment import Shipment
from apps.accounts.models import User


class ShipmentEvent(BaseModel):

    class EventType(models.TextChoices):
        CREATED = "CREATED", "Created"
        DRIVER_ASSIGNED = "DRIVER_ASSIGNED", "Driver Assigned"
        PICKED_UP = "PICKED_UP", "Picked Up"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
    )

    description = models.TextField()

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.shipment.tracking_number} - "
            f"{self.event_type}"
        )