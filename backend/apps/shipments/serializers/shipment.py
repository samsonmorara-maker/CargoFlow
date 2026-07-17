from rest_framework import serializers
from apps.shipments.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipment

        fields = "__all__"

        read_only_fields = (
            "uuid",
            "tracking_number",
            "customer",
            "driver",
            "status",
            "final_price",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "is_deleted",
            "deleted_at",
        )