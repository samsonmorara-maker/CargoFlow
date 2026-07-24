from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField()

    new_password = serializers.CharField(
        min_length=8
    )