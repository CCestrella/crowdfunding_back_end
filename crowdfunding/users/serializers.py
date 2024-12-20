from rest_framework import serializers
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Dynamically references the custom user model
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
