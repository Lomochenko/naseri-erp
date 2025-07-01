from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    model_name = models.CharField(max_length=255)
    object_id = models.IntegerField()
    action = models.CharField(max_length=50)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.model_name} by {self.changed_by}"