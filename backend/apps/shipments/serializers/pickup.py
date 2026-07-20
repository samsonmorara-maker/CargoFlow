from rest_framework import serializers


class PickupSerializer(serializers.Serializer):
    pickup_qr_token = serializers.UUIDField()