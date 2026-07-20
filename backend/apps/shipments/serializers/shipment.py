from rest_framework import serializers
from apps.shipments.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):

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