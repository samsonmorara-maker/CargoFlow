from rest_framework import serializers


class AssignmentResponseSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)