from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User, DriverProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    ordering = ("email",)

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
                "profile_picture",
            )
        }),
        ("Role", {
            "fields": (
                "role",
                "is_verified",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "verification_status",
        "availability_status",
        "rating",
        "completed_deliveries",
    )

    list_filter = (
        "verification_status",
        "availability_status",
    )

    search_fields = (
        "user__email",
        "license_number",
    )