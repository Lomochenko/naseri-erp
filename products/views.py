from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Unit, Product
from .serializers import (
    CategorySerializer, UnitSerializer,
    ProductSerializer, ProductListSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Category instances."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Unit instances."""
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'symbol']
    ordering_fields = ['name']
    ordering = ['name']

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Product instances."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'purchase_price', 'selling_price', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Return products with stock below minimum level."""
        products = []
        for product in Product.objects.filter(is_active=True):
            if product.current_stock <= product.min_stock:
                products.append(product)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
