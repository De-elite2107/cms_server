from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password', 'address', 'dob', 'occupation', 'wedding', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Check that the email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        """Check that the username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user