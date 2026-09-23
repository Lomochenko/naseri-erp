from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Activity, AuditLog
from .serializers import ActivitySerializer, AuditLogSerializer
from .utils import (
    get_recent_activities, get_unread_activities, 
    mark_activities_as_read, get_activity_summary
)

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing activities and notifications
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Activity.objects.select_related('user', 'content_type')
        
        # Filter by activity type
        activity_type = self.request.query_params.get('type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Search in title and description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent activities for current user
        """
        limit = int(request.query_params.get('limit', 20))
        activities = get_recent_activities(user=request.user, limit=limit)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """
        Get unread activities for current user
        """
        activities = get_unread_activities(request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        """
        Mark activities as read
        """
        activity_ids = request.data.get('activity_ids', [])
        count = mark_activities_as_read(request.user, activity_ids)
        
        return Response({
            'success': True,
            'message': f'{count} فعالیت به عنوان خوانده‌شده علامت‌گذاری شد',
            'marked_count': count
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get activity summary for dashboard
        """
        days = int(request.query_params.get('days', 7))
        summary = get_activity_summary(user=request.user, days=days)
        
        return Response({
            'success': True,
            'data': summary
        })

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        """
        Get notifications for header notification menu
        """
        # Get unread high priority activities
        notifications = Activity.objects.filter(
            requires_notification=True,
            is_read=False,
            priority__in=['high', 'critical']
        ).select_related('user', 'content_type')[:10]
        
        # Also get recent activities regardless of read status
        recent = Activity.objects.select_related('user', 'content_type')[:20]
        
        return Response({
            'notifications': ActivitySerializer(notifications, many=True).data,
            'recent_activities': ActivitySerializer(recent, many=True).data,
            'unread_count': notifications.count()
        })

    @action(detail=False, methods=['get'])
    def system_activities(self, request):
        """
        Get all system activities (for admin users)
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'دسترسی محدود به مدیران سیستم'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        activities = Activity.objects.select_related('user', 'content_type')
        serializer = self.get_serializer(activities, many=True)
        
        return Response(serializer.data)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Legacy audit log viewset
    """
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
