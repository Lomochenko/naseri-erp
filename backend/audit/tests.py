from django.test import TestCase
from audit.models import AuditLog
from users.models import User

class AuditLogTest(TestCase):
    def test_create_audit_log(self):
        user = User.objects.create_user(phone_number='09123456789', password='testpassword')
        log = AuditLog.objects.create(
            model_name='User',
            object_id=user.id,
            action='created',
            changed_by=user
        )
        self.assertEqual(log.model_name, 'User')
        self.assertEqual(log.action, 'created')