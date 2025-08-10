from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import json

class ProductHistory(models.Model):
    """Model for tracking all changes made to products."""
    ACTION_CHOICES = [
        ('create', _('Created')),
        ('update', _('Updated')),
        ('delete', _('Deleted')),
    ]
    
    # Product reference
    product = models.ForeignKey('Product', verbose_name=_('product'), 
                               on_delete=models.CASCADE, 
                               related_name='history')
    
    # Action details
    action = models.CharField(_('action'), max_length=20, choices=ACTION_CHOICES)
    changes = models.JSONField(_('changes'), default=dict, blank=True)
    old_values = models.JSONField(_('old values'), default=dict, blank=True)
    new_values = models.JSONField(_('new values'), default=dict, blank=True)
    
    # User and timestamp
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                            on_delete=models.PROTECT, related_name='product_histories')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    # Optional notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('product history')
        verbose_name_plural = _('product histories')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.product.name} - {self.get_action_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def formatted_changes(self):
        """Return human-readable changes."""
        if not self.changes:
            return {}
            
        field_names = {
            'name': 'نام محصول',
            'code': 'کد محصول',
            'description': 'توضیحات',
            'purchase_price': 'قیمت خرید',
            'selling_price': 'قیمت فروش',
            'min_stock': 'حداقل موجودی',
            'max_stock': 'حداکثر موجودی',
            'category': 'دسته‌بندی',
            'unit': 'واحد',
            'is_active': 'وضعیت فعالیت',
        }
        
        formatted = {}
        for field, change in self.changes.items():
            field_name = field_names.get(field, field)
            formatted[field_name] = change
            
        return formatted
