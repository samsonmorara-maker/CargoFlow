from rest_framework import serializers


class PickupDetailsSerializer(serializers.Serializer):
    tracking_number = serializers.CharField()
    pickup_qr_token = serializers.UUIDField()
    pickup_code = serializers.CharField()   
    pickup_address = serializers.CharField()

    driver_name = serializers.CharField(required=False)
    driver_phone = serializers.CharField(required=False)
    vehicle_type = serializers.CharField(required=False)
    vehicle_number_plate = serializers.CharField(required=False)


class DeliveryDetailsSerializer(serializers.Serializer):
    tracking_number = serializers.CharField()
    delivery_qr_token = serializers.UUIDField()
    delivery_code = serializers.CharField()
    delivery_address = serializers.CharField()
    estimated_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )