from rest_framework import serializers

from apps.shipments.models import Shipment
from apps.shipments.serializers import ShipmentEventSerializer


class TrackingSerializer(serializers.ModelSerializer):
    events = ShipmentEventSerializer(
        many=True,
        read_only=True,
    )

    driver_name = serializers.SerializerMethodField()
    driver_phone = serializers.SerializerMethodField()

    vehicle_type = serializers.SerializerMethodField()
    vehicle_color = serializers.SerializerMethodField()
    vehicle_number_plate = serializers.SerializerMethodField()

    customer = serializers.SerializerMethodField()

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

            "driver_name",
            "driver_phone",

            "vehicle_type",
            "vehicle_color",
            "vehicle_number_plate",

            "customer",

            "events",
        )

    def get_driver_name(self, obj):
        if obj.driver:
            return f"{obj.driver.first_name} {obj.driver.last_name}"
        return None

    def get_driver_phone(self, obj):
        if obj.driver:
            return obj.driver.phone_number
        return None

    def get_vehicle_type(self, obj):
        if obj.driver and hasattr(obj.driver, "vehicle"):
            return obj.driver.vehicle.vehicle_type
        return None

    def get_vehicle_color(self, obj):
        if obj.driver and hasattr(obj.driver, "vehicle"):
            return obj.driver.vehicle.color
        return None

    def get_vehicle_number_plate(self, obj):
        if obj.driver and hasattr(obj.driver, "vehicle"):
            return obj.driver.vehicle.number_plate
        return None

    def get_customer(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"