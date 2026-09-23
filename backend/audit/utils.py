"""
Activity tracking utilities for comprehensive user activity logging
"""
from .models import Activity
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import json


def log_activity(activity_type, title, user=None, content_object=None, description='', 
                 priority='medium', metadata=None, request=None):
    """
    Log an activity to the system
    
    Args:
        activity_type (str): Type of activity from ACTIVITY_TYPES choices
        title (str): Title of the activity
        user: User who performed the activity
        content_object: Related model instance (optional)
        description (str): Detailed description
        priority (str): Priority level ('low', 'medium', 'high', 'critical')
        metadata (dict): Additional data as JSON
        request: HTTP request object for IP and user agent
    
    Returns:
        Activity: Created activity instance
    """
    activity_data = {
        'activity_type': activity_type,
        'title': title,
        'description': description,
        'user': user,
        'priority': priority,
        'metadata': metadata or {}
    }
    
    # Set content object if provided
    if content_object:
        activity_data['content_type'] = ContentType.objects.get_for_model(content_object)
        activity_data['object_id'] = content_object.pk
    
    # Extract request information
    if request:
        activity_data['ip_address'] = get_client_ip(request)
        activity_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
    
    return Activity.objects.create(**activity_data)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_user_activity(user, activity_type, title, description='', priority='medium', metadata=None, request=None):
    """Log user-specific activities"""
    return log_activity(
        activity_type=activity_type,
        title=title,
        user=user,
        description=description,
        priority=priority,
        metadata=metadata,
        request=request
    )


def log_model_activity(user, model_instance, activity_type, title, description='', priority='medium', metadata=None, request=None):
    """Log activities related to model instances"""
    return log_activity(
        activity_type=activity_type,
        title=title,
        user=user,
        content_object=model_instance,
        description=description,
        priority=priority,
        metadata=metadata,
        request=request
    )


def get_recent_activities(user=None, limit=20):
    """Get recent activities, optionally filtered by user"""
    queryset = Activity.objects.select_related('user', 'content_type')
    
    if user:
        queryset = queryset.filter(user=user)
    
    return queryset[:limit]


def get_unread_activities(user):
    """Get unread activities for a user"""
    return Activity.objects.filter(
        user=user,
        is_read=False,
        requires_notification=True
    ).select_related('content_type')


def mark_activities_as_read(user, activity_ids=None):
    """Mark activities as read for a user"""
    queryset = Activity.objects.filter(user=user, is_read=False)
    
    if activity_ids:
        queryset = queryset.filter(id__in=activity_ids)
    
    return queryset.update(is_read=True)


# Activity logging decorators and middleware helpers

def log_login_activity(user, request):
    """Log user login activity"""
    return log_user_activity(
        user=user,
        activity_type='user_login',
        title=f'{user.get_full_name() or user.phone_number} وارد سیستم شد',
        description=f'کاربر از IP {get_client_ip(request)} وارد شده است',
        priority='low',
        metadata={'login_time': timezone.now().isoformat()},
        request=request
    )


def log_logout_activity(user, request):
    """Log user logout activity"""
    return log_user_activity(
        user=user,
        activity_type='user_logout',
        title=f'{user.get_full_name() or user.phone_number} از سیستم خارج شد',
        priority='low',
        request=request
    )


def log_product_activity(user, product, action, request=None):
    """Log product-related activities"""
    action_map = {
        'create': ('product_created', f'محصول جدید "{product.name}" ایجاد شد'),
        'update': ('product_updated', f'محصول "{product.name}" بروزرسانی شد'),
        'delete': ('product_deleted', f'محصول "{product.name}" حذف شد'),
        'view': ('product_viewed', f'محصول "{product.name}" مشاهده شد')
    }
    
    if action in action_map:
        activity_type, title = action_map[action]
        return log_model_activity(
            user=user,
            model_instance=product,
            activity_type=activity_type,
            title=title,
            metadata={
                'product_code': product.code,
                'category': product.category.name if product.category else None,
                'price': str(product.selling_price)
            },
            request=request
        )


def log_customer_activity(user, customer, action, request=None):
    """Log customer-related activities"""
    action_map = {
        'create': ('customer_created', f'مشتری جدید "{customer.name}" ایجاد شد'),
        'update': ('customer_updated', f'اطلاعات مشتری "{customer.name}" بروزرسانی شد'),
        'delete': ('customer_deleted', f'مشتری "{customer.name}" حذف شد')
    }
    
    if action in action_map:
        activity_type, title = action_map[action]
        return log_model_activity(
            user=user,
            model_instance=customer,
            activity_type=activity_type,
            title=title,
            metadata={
                'customer_code': customer.customer_code,
                'phone': customer.phone,
                'customer_type': customer.customer_type
            },
            request=request
        )


def log_sale_activity(user, sale, action, request=None):
    """Log sale-related activities"""
    action_map = {
        'create': ('sale_created', f'فاکتور جدید "{sale.invoice_number}" ایجاد شد'),
        'confirm': ('sale_confirmed', f'فاکتور "{sale.invoice_number}" تأیید شد'),
        'complete': ('sale_completed', f'فاکتور "{sale.invoice_number}" تکمیل شد'),
        'cancel': ('sale_cancelled', f'فاکتور "{sale.invoice_number}" لغو شد'),
        'update': ('sale_updated', f'فاکتور "{sale.invoice_number}" بروزرسانی شد')
    }
    
    if action in action_map:
        activity_type, title = action_map[action]
        priority = 'high' if action in ['confirm', 'complete'] else 'medium'
        
        return log_model_activity(
            user=user,
            model_instance=sale,
            activity_type=activity_type,
            title=title,
            priority=priority,
            metadata={
                'customer': sale.customer.name,
                'total': str(sale.total),
                'status': sale.status,
                'items_count': sale.items.count()
            },
            request=request
        )


def log_inventory_activity(user, activity_type, title, product=None, quantity=None, metadata=None, request=None):
    """Log inventory-related activities"""
    activity_metadata = metadata or {}
    
    if product and quantity is not None:
        activity_metadata.update({
            'product_name': product.name,
            'product_code': product.code,
            'quantity': str(quantity),
            'current_stock': str(product.current_stock)
        })
    
    priority = 'high' if activity_type == 'stock_low_warning' else 'medium'
    
    return log_activity(
        activity_type=activity_type,
        title=title,
        user=user,
        content_object=product,
        priority=priority,
        metadata=activity_metadata,
        request=request
    )


def log_system_activity(activity_type, title, user=None, description='', priority='medium', metadata=None):
    """Log system-level activities"""
    return log_activity(
        activity_type=activity_type,
        title=title,
        user=user,
        description=description,
        priority=priority,
        metadata=metadata
    )


def get_activity_summary(user=None, days=7):
    """Get activity summary for dashboard"""
    from datetime import timedelta
    from django.utils import timezone
    from django.db.models import Count
    
    start_date = timezone.now() - timedelta(days=days)
    queryset = Activity.objects.filter(created_at__gte=start_date)
    
    if user:
        queryset = queryset.filter(user=user)
    
    # Group by activity type
    summary = queryset.values('activity_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Get priority breakdown
    priority_summary = queryset.values('priority').annotate(
        count=Count('id')
    )
    
    return {
        'total_activities': queryset.count(),
        'by_type': list(summary),
        'by_priority': list(priority_summary),
        'recent_activities': queryset.select_related('user', 'content_type')[:10]
    }