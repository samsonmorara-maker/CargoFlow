from django.contrib import admin

from apps.shipments.models import Shipment
from apps.shipments.models import ShipmentEvent

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

@admin.register(ShipmentEvent)
class ShipmentEventAdmin(admin.ModelAdmin):
    list_display = (
        "shipment",
        "event_type",
        "performed_by",
        "created_at",
    )

    list_filter = (
        "event_type",
        "created_at",
    )

    search_fields = (
        "shipment__tracking_number",
        "description",
    )