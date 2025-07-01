from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AuditLog
from users.models import User
from products.models import Product
from accounting.models import Transaction

@receiver(post_save, sender=User)
@receiver(post_save, sender=Product)
@receiver(post_save, sender=Transaction)
def log_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    AuditLog.objects.create(
        model_name=sender.__name__,
        object_id=instance.id,
        action=action,
        changed_by=instance.changed_by if hasattr(instance, 'changed_by') else None
    )

@receiver(post_delete, sender=User)
@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=Transaction)
def log_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        model_name=sender.__name__,
        object_id=instance.id,
        action="deleted",
        changed_by=instance.changed_by if hasattr(instance, 'changed_by') else None
    )