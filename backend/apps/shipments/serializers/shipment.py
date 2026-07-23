from rest_framework import serializers
from apps.shipments.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    driver_phone = serializers.SerializerMethodField()

    vehicle_type = serializers.SerializerMethodField()
    vehicle_color = serializers.SerializerMethodField()
    vehicle_number_plate = serializers.SerializerMethodField()
    class Meta:
        model = Shipment

        fields = (
        "id",
        "uuid",
        "tracking_number",
        "goods_type",
        "package_name",
        "description",
        "quantity",
        "weight",
        "declared_value",
        "is_fragile",
        "pickup_address",
        "delivery_address",
        "priority",
        "estimated_price",
        "final_price",
        "status",
        "delivery_instructions",
        "pickup_confirmed_at",
        "delivery_confirmed_at",
        "customer",
        "driver",
        "created_at",
        "updated_at",
        "driver_name",
        "driver_phone",
        "vehicle_type",
        "vehicle_color",
        "vehicle_number_plate",
        )

        read_only_fields = (
        "id",
        "uuid",
        "tracking_number",
        "status",
        "pickup_confirmed_at",
        "delivery_confirmed_at",
        "created_at",
        "updated_at",
        "customer",
        "driver",
        
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