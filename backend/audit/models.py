from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import json

class Activity(models.Model):
    """Comprehensive activity tracking model"""
    ACTIVITY_TYPES = [
        # User activities
        ('user_login', 'ورود کاربر'),
        ('user_logout', 'خروج کاربر'),
        ('user_created', 'ایجاد کاربر جدید'),
        ('user_updated', 'بروزرسانی کاربر'),
        ('user_deleted', 'حذف کاربر'),
        
        # Product activities
        ('product_created', 'ایجاد محصول جدید'),
        ('product_updated', 'بروزرسانی محصول'),
        ('product_deleted', 'حذف محصول'),
        ('product_viewed', 'مشاهده محصول'),
        
        # Category activities
        ('category_created', 'ایجاد دسته‌بندی جدید'),
        ('category_updated', 'بروزرسانی دسته‌بندی'),
        ('category_deleted', 'حذف دسته‌بندی'),
        
        # Customer activities
        ('customer_created', 'ایجاد مشتری جدید'),
        ('customer_updated', 'بروزرسانی اطلاعات مشتری'),
        ('customer_deleted', 'حذف مشتری'),
        
        # Sales activities
        ('sale_created', 'ایجاد فاکتور جدید'),
        ('sale_confirmed', 'تأیید فاکتور فروش'),
        ('sale_completed', 'تکمیل فاکتور فروش'),
        ('sale_cancelled', 'لغو فاکتور فروش'),
        ('sale_updated', 'بروزرسانی فاکتور'),
        ('receipt_generated', 'تولید رسید'),
        ('receipt_printed', 'چاپ رسید'),
        
        # Inventory activities
        ('stock_adjustment', 'تعدیل موجودی'),
        ('stock_low_warning', 'هشدار موجودی کم'),
        ('inventory_transaction', 'تراکنش موجودی'),
        
        # Purchase activities
        ('purchase_created', 'ایجاد سفارش خرید'),
        ('purchase_confirmed', 'تأیید سفارش خرید'),
        ('purchase_received', 'دریافت کالا'),
        ('purchase_cancelled', 'لغو سفارش خرید'),
        
        # Payment activities
        ('payment_received', 'دریافت پرداخت'),
        ('payment_made', 'انجام پرداخت'),
        ('payment_cancelled', 'لغو پرداخت'),
        
        # System activities
        ('backup_created', 'تهیه پشتیبان'),
        ('report_generated', 'تولید گزارش'),
        ('system_error', 'خطای سیستم'),
        ('data_export', 'صادرات داده‌ها'),
        ('data_import', 'واردات داده‌ها'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
        ('critical', 'بحرانی'),
    ]
    
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=255, help_text="عنوان فعالیت")
    description = models.TextField(blank=True, help_text="توضیحات تفصیلی")
    
    # Generic foreign key for relating to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='activities', help_text="کاربر انجام‌دهنده")
    
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    
    # Additional context data
    metadata = models.JSONField(default=dict, blank=True,
                               help_text="اطلاعات اضافی در فرمت JSON")
    
    # IP and device info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Notification status
    is_read = models.BooleanField(default=False)
    requires_notification = models.BooleanField(default=True)
    notification_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'فعالیت'
        verbose_name_plural = 'فعالیت‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['activity_type', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
            models.Index(fields=['is_read', 'requires_notification']),
        ]
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title}"
    
    @property
    def is_recent(self):
        """Check if activity is recent (within last 24 hours)"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(hours=24)
    
    @property
    def formatted_time(self):
        """Return formatted time for display"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - self.created_at
        
        if diff < timedelta(minutes=1):
            return "هم‌اکنون"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} دقیقه پیش"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} ساعت پیش"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} روز پیش"
        else:
            return self.created_at.strftime('%Y/%m/%d')

class AuditLog(models.Model):
    """Legacy audit log model - kept for backward compatibility"""
    model_name = models.CharField(max_length=255)
    object_id = models.IntegerField()
    action = models.CharField(max_length=50)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.model_name} by {self.changed_by}"
