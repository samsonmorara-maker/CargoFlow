from rest_framework import serializers


class CancelShipmentSerializer(serializers.Serializer):
    reason = serializers.CharField(
        max_length=500,
    )