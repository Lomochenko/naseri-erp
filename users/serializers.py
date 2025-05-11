from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'email', 
                  'is_active', 'is_staff', 'is_manager', 'password', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user
    
    def update(self, instance, validated_data):
        """Update user, setting the password correctly if needed."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'phone_number']

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        """Validate that the old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Old password is incorrect.'))
        return value
    
    def validate_new_password(self, value):
        """Validate the new password."""
        # Add password validation logic here if needed
        if len(value) < 8:
            raise serializers.ValidationError(_('Password must be at least 8 characters long.'))
        return value

class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
