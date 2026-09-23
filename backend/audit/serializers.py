from rest_framework import serializers
from .models import Activity, AuditLog
from users.serializers import UserSerializer

class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for Activity model with detailed information
    """
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    formatted_time = serializers.CharField(read_only=True)
    is_recent = serializers.BooleanField(read_only=True)
    
    # Related object information
    content_type_name = serializers.SerializerMethodField()
    object_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'activity_type', 'activity_type_display',
            'title', 'description', 'priority', 'priority_display',
            'user_name', 'user_avatar', 'metadata',
            'ip_address', 'user_agent',
            'is_read', 'requires_notification', 'notification_sent',
            'created_at', 'formatted_time', 'is_recent',
            'content_type_name', 'object_name'
        ]
        read_only_fields = [
            'id', 'created_at', 'formatted_time', 'is_recent',
            'activity_type_display', 'priority_display',
            'user_name', 'user_avatar', 'content_type_name', 'object_name'
        ]
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.phone_number
        return 'نامشخص'
    
    def get_user_avatar(self, obj):
        # Return a default avatar or user avatar if available
        return '/images/user/default-avatar.png'  # You can customize this
    
    def get_content_type_name(self, obj):
        if obj.content_type:
            return obj.content_type.name
        return None
    
    def get_object_name(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return None

class ActivitySummarySerializer(serializers.Serializer):
    """
    Serializer for activity summary data
    """
    total_activities = serializers.IntegerField()
    by_type = serializers.ListField(
        child=serializers.DictField()
    )
    by_priority = serializers.ListField(
        child=serializers.DictField()
    )
    recent_activities = ActivitySerializer(many=True)

class NotificationSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for notifications in header menu
    """
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    formatted_time = serializers.CharField(read_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'activity_type', 'activity_type_display',
            'title', 'priority', 'user_name', 'user_image',
            'formatted_time', 'is_read', 'created_at'
        ]
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.phone_number
        return 'سیستم'
    
    def get_user_image(self, obj):
        return '/images/user/default-avatar.png'

class AuditLogSerializer(serializers.ModelSerializer):
    """
    Legacy audit log serializer - kept for backward compatibility
    """
    changed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = ['id', 'model_name', 'object_id', 'action', 
                 'changed_by', 'changed_by_name', 'timestamp']
    
    def get_changed_by_name(self, obj):
        if obj.changed_by:
            return obj.changed_by.get_full_name() or obj.changed_by.phone_number
        return None
