from rest_framework import serializers

from apps.shipments.models import ShipmentEvent


class ShipmentEventSerializer(serializers.ModelSerializer):
    performed_by = serializers.SerializerMethodField()

    class Meta:
        model = ShipmentEvent

        fields = (
            "event_type",
            "description",
            "performed_by",
            "created_at",
        )

    def get_performed_by(self, obj):
        if obj.performed_by:
            return (
                f"{obj.performed_by.first_name} "
                f"{obj.performed_by.last_name}"
            )

        return "System"