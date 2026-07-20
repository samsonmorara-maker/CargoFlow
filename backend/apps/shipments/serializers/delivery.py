from rest_framework import serializers


class DeliverySerializer(serializers.Serializer):
    delivery_qr_token = serializers.UUIDField(required=False)
    delivery_code = serializers.CharField(required=False)

    received_by_name = serializers.CharField(
        max_length=255,
        required=True,
    )

    received_by_phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )
    

    def validate(self, attrs):
        if not attrs.get("delivery_qr_token") and not attrs.get("delivery_code"):
            raise serializers.ValidationError(
                "Provide either a delivery QR token or a delivery code."
            )

        return attrs