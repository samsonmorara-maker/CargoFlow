from rest_framework import serializers


class DeliverySerializer(serializers.Serializer):
    delivery_qr_token = serializers.UUIDField(
        required=False
    )

    delivery_code = serializers.CharField(
        required=False
    )

    def validate(self, attrs):
        if not attrs.get("delivery_qr_token") and not attrs.get("delivery_code"):
            raise serializers.ValidationError(
                "Provide either a delivery QR token or a delivery code."
            )

        return attrs