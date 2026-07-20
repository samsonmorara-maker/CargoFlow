from rest_framework import serializers

from apps.shipments.models import Shipment
from apps.shipments.serializers import ShipmentEventSerializer


class TrackingSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    events = ShipmentEventSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Shipment

        fields = (
            "tracking_number",
            "status",
            "goods_type",
            "package_name",
            "pickup_address",
            "delivery_address",
            "estimated_price",
            "driver",
            "customer",
            "events",
        )

    def get_driver(self, obj):
        if obj.driver:
            return (
                f"{obj.driver.first_name} "
                f"{obj.driver.last_name}"
            )

        return None

    def get_customer(self, obj):
        return (
            f"{obj.customer.first_name} "
            f"{obj.customer.last_name}"
        )