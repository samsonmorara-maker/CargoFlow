from rest_framework import serializers
from apps.accounts.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle

        fields = (
            "id",
            "vehicle_type",
            "make",
            "model",
            "color",
            "number_plate",
            "year",
            "is_active",
        )

        read_only_fields = (
            "id",
            "is_active",
        )