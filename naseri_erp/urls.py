"""
URL configuration for naseri_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API documentation setup with Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="یراق‌آلات ناصری API",
        default_version='v1',
        description="API documentation for Yaraghalat Naseri ERP system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    # Temporarily commented out until views are implemented
    # path('api/inventory/', include('inventory.urls')),
    # path('api/sales/', include('sales.urls')),
    # path('api/purchases/', include('purchases.urls')),
    # path('api/accounting/', include('accounting.urls')),

    # REST framework authentication
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
