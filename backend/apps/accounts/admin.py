from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import DriverProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "phone_number",
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
        "phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "uuid",
    )

    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password",
            )
        }),
        ("Profile", {
            "fields": (
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
        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
                "uuid",
                "last_login",
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