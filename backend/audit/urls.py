from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'logs', AuditLogViewSet, basename='auditlog')

urlpatterns = router.urls
