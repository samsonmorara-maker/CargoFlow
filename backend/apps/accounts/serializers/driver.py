from rest_framework import serializers
from apps.accounts.models import User
from apps.shipments.models import Shipment


class DriverSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.SerializerMethodField()
    number_plate = serializers.SerializerMethodField()
    completed_deliveries = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id",
            "uuid",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_verified",
            "is_active",
            "vehicle_type",
            "number_plate",
            "completed_deliveries",
        )

    def get_vehicle_type(self, obj):
        if hasattr(obj, "vehicle"):
            return obj.vehicle.vehicle_type
        return None

    def get_number_plate(self, obj):
        if hasattr(obj, "vehicle"):
            return obj.vehicle.number_plate
        return None

    from apps.shipments.models import Shipment

    def get_completed_deliveries(self, obj):
        return obj.assigned_shipments.filter(
        status=Shipment.Status.DELIVERED
        ).count()
        