from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
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
    
    def create(self, request, *args, **kwargs):
        """Create product and handle initial stock if provided."""
        # Extract current_stock from request data
        current_stock = request.data.get('current_stock', 0)
        
        # Create the product first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        # Create initial stock transaction if current_stock > 0
        if current_stock and float(current_stock) > 0:
            from inventory.models import InventoryTransaction, Warehouse
            
            # Get or create default warehouse
            warehouse, created = Warehouse.objects.get_or_create(
                name='انبار اصلی',
                defaults={
                    'location': 'محل اصلی',
                    'description': 'انبار پیش‌فرض سیستم',
                    'is_active': True
                }
            )
            
            # Create inventory transaction for initial stock
            InventoryTransaction.objects.create(
                transaction_type='purchase',
                product=product,
                warehouse=warehouse,
                quantity=Decimal(str(current_stock)),
                unit_price=product.purchase_price,
                reference_number=f'INIT-{product.code}',
                reference_type='initial_stock',
                notes=f'موجودی اولیه محصول {product.name}',
                created_by=request.user
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
