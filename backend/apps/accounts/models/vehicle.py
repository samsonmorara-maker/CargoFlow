from django.db import models
from django.core.validators import MinLengthValidator
from apps.common.models import BaseModel
from apps.accounts.models.user import User


class Vehicle(BaseModel):

    class VehicleCategory(models.TextChoices):
        TRUCK = "TRUCK", "Truck"
        VAN = "VAN", "Van"
        CAR = "CAR", "Car"
        MOTORCYCLE = "MOTORCYCLE", "Motorcycle"
        BICYCLE = "BICYCLE", "Bicycle"
        SCOOTER = "SCOOTER", "Scooter"
        WALKING = "WALKING", "Walking"

    class OwnershipType(models.TextChoices):
        OWNER = "OWNER", "Owner"
        COMPANY = "COMPANY", "Company Vehicle"
        RENTAL = "RENTAL", "Rental"
        BORROWED = "BORROWED", "Borrowed"

    driver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vehicle",
    )

    category = models.CharField(
        max_length=20,
        choices=VehicleCategory.choices,
    )

    ownership_type = models.CharField(
        max_length=20,
        choices=OwnershipType.choices,
        default=OwnershipType.OWNER,
    )

    make = models.CharField(
        max_length=100,
        blank=True,
    )

    model = models.CharField(
        max_length=100,
        blank=True,
    )

    color = models.CharField(
        max_length=50,
        blank=True,
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    number_plate = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    owner_name = models.CharField(
        max_length=255,
        blank=True,
    )

    owner_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    registration_document = models.FileField(
        upload_to="vehicle_documents/",
        blank=True,
        null=True,
    )

    insurance_document = models.FileField(
        upload_to="vehicle_documents/",
        blank=True,
        null=True,
    )

    inspection_certificate = models.FileField(
        upload_to="vehicle_documents/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.driver.email} - {self.category}"