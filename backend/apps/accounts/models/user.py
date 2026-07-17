from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.common.models import BaseModel
from apps.accounts.managers import UserManager


class User( BaseModel, AbstractBaseUser, PermissionsMixin ):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        DRIVER = "DRIVER", "Driver"
        ADMIN = "ADMIN", "Admin"
    
    username = None

    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        db_index=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        

    def __str__(self):
        return f"{self.email} ({self.role})"