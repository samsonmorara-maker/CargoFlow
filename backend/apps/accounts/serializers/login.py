from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.accounts.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        # DEBUG
        try:
            user = User.objects.get(email=email)
            print("User exists:", user.email)
            print("Password matches:", user.check_password(password))
            print("Is active:", user.is_active)
        except User.DoesNotExist:
            print("User does not exist")

        user = authenticate(
            username=email,
            password=password,
        )

        print("Authenticate returned:", user)

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        attrs["user"] = user
        return attrs