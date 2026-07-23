from django.db import models
from django.core.validators import MinLengthValidator
from apps.common.models import BaseModel
from apps.accounts.models.user import User


class Vehicle(BaseModel):

    driver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vehicle",
    )

    vehicle_type = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        help_text="Example: Toyota Hiace, Mercedes Sprinter, Box Truck",
    )

    make = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    color = models.CharField(max_length=50)

    number_plate = models.CharField(
        max_length=20,
        unique=True,
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.number_plate