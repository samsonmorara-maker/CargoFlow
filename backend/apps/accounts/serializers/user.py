from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            "uuid",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_staff", 
            "profile_picture",
            "is_verified",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "uuid",
            "is_staff", 
            "is_verified",
            "created_at",
            "updated_at",
        )