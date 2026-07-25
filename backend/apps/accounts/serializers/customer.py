from rest_framework import serializers
from apps.accounts.models import User


class CustomerSerializer(serializers.ModelSerializer):
    total_shipments = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "uuid",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "total_shipments",
        )