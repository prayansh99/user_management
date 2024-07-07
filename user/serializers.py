from rest_framework import serializers
import re

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, max_length=100)

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError("Username must be alphanumeric.")
        return value

    def validate_first_name(self, value):
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("Last name must contain only letters.")
        return value
