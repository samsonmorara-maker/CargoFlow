from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    total_shipments = serializers.IntegerField()

    pending_shipments = serializers.IntegerField()

    driver_assigned = serializers.IntegerField()

    in_transit = serializers.IntegerField()

    delivered = serializers.IntegerField()

    cancelled = serializers.IntegerField()

    total_customers = serializers.IntegerField()

    total_drivers = serializers.IntegerField()

    available_drivers = serializers.IntegerField()

    busy_drivers = serializers.IntegerField()

    offline_drivers = serializers.IntegerField()