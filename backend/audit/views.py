from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    def get(self, request):
        logs = AuditLog.objects.all()
        data = [
            {
                'model_name': log.model_name,
                'object_id': log.object_id,
                'action': log.action,
                'changed_by': log.changed_by.username if log.changed_by else None,
                'timestamp': log.timestamp
            }
            for log in logs
        ]
        return Response(data)