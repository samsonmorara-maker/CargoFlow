from rest_framework import serializers


class DriverDashboardSerializer(serializers.Serializer):
    pending_pickups = serializers.IntegerField()
    active_deliveries = serializers.IntegerField()
    in_transit = serializers.IntegerField()
    completed_today = serializers.IntegerField()
    total_completed = serializers.IntegerField()