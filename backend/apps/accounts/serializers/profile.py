from rest_framework import serializers

from apps.accounts.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            "uuid",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_picture",
            "role",
            "created_at",
        )

        read_only_fields = (
            "uuid",
            "email",
            "role",
            "created_at",
        )