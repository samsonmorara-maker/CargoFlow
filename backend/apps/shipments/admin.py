from django.contrib import admin

from apps.shipments.models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_number",
        "customer",
        "goods_type",
        "status",
        "priority",
        "estimated_price",
    )

    list_filter = (
        "status",
        "priority",
        "goods_type",
    )

    search_fields = (
        "tracking_number",
        "package_name",
        "customer__email",
    )