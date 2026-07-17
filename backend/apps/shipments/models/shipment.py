from django.db import models
from django.utils import timezone
from apps.common.models import BaseModel
from apps.accounts.models import User


class Shipment(BaseModel):

    class GoodsType(models.TextChoices):
        DOCUMENT = "DOCUMENT", "Document"
        FOOD = "FOOD", "Food"
        GROCERIES = "GROCERIES", "Groceries"
        ELECTRONICS = "ELECTRONICS", "Electronics"
        CLOTHING = "CLOTHING", "Clothing"
        FURNITURE = "FURNITURE", "Furniture"
        MEDICINE = "MEDICINE", "Medicine"
        CONSTRUCTION = "CONSTRUCTION", "Construction Materials"
        INDUSTRIAL = "INDUSTRIAL", "Industrial Equipment"
        AGRICULTURE = "AGRICULTURE", "Agricultural Products"
        FRAGILE = "FRAGILE", "Fragile Goods"
        HAZARDOUS = "HAZARDOUS", "Hazardous Goods"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        DRIVER_ASSIGNED = "DRIVER_ASSIGNED", "Driver Assigned"
        PICKED_UP = "PICKED_UP", "Picked Up"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    class Priority(models.TextChoices):
        STANDARD = "STANDARD", "Standard"
        EXPRESS = "EXPRESS", "Express"
        SAME_DAY = "SAME_DAY", "Same Day"

    tracking_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipments",
    )

    goods_type = models.CharField(
        max_length=30,
        choices=GoodsType.choices,
        default=GoodsType.OTHER,
    )

    package_name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    quantity = models.PositiveIntegerField(default=1)

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    declared_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    is_fragile = models.BooleanField(default=False)

    pickup_address = models.TextField()

    delivery_address = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.STANDARD,
    )

    estimated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    delivery_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.package_name}"
    

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            year = timezone.now().year

            last_shipment = (
                Shipment.objects.filter(
                 tracking_number__startswith=f"CFG{year}"
                )
                .order_by("-tracking_number")
                .first()
            )

            if last_shipment:
                last_number = int(last_shipment.tracking_number[-6:])
                next_number = last_number + 1
            else:
                next_number = 1

            self.tracking_number = f"CFG{year}{next_number:06d}"

        super().save(*args, **kwargs)