from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Creating a router for Products
product_router = DefaultRouter()
product_router.register('', views.ProductViewSet)

# Creating separate routers for Categories and Units
category_router = DefaultRouter()
category_router.register('', views.CategoryViewSet)

unit_router = DefaultRouter()
unit_router.register('', views.UnitViewSet)

# Using the URLs from the routers
urlpatterns = [
    # Categories API endpoint
    path('categories/', include(category_router.urls)),
    # Units API endpoint
    path('units/', include(unit_router.urls)),
    # Products API endpoint (base path)
    path('', include(product_router.urls)),
]
