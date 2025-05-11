from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from .models import Warehouse, InventoryTransaction, StockAdjustment, StockAdjustmentItem
from products.models import Product

# Placeholder for serializers - we'll create these later
class WarehouseSerializer:
    class Meta:
        model = Warehouse
        fields = '__all__'

class InventoryTransactionSerializer:
    class Meta:
        model = InventoryTransaction
        fields = '__all__'

class StockAdjustmentSerializer:
    class Meta:
        model = StockAdjustment
        fields = '__all__'

class StockAdjustmentItemSerializer:
    class Meta:
        model = StockAdjustmentItem
        fields = '__all__'

class WarehouseViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Warehouse instances."""
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing InventoryTransaction instances."""
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'product', 'warehouse']
    search_fields = ['reference_number', 'notes']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class StockAdjustmentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing StockAdjustment instances."""
    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['adjustment_type', 'warehouse']
    search_fields = ['reason']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class StockAdjustmentItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing StockAdjustmentItem instances."""
    queryset = StockAdjustmentItem.objects.all()
    serializer_class = StockAdjustmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['adjustment', 'product']
    search_fields = ['notes']

class ProductStockView(generics.RetrieveAPIView):
    """API view for retrieving product stock information."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        """Handle GET requests for product stock."""
        try:
            product = Product.objects.get(id=product_id)
            stock_data = {
                'product_id': product.id,
                'product_name': product.name,
                'product_code': product.code,
                'current_stock': product.current_stock,
                'min_stock': product.min_stock,
                'unit': product.unit.symbol,
                'warehouses': []
            }

            # Get stock by warehouse
            warehouses = Warehouse.objects.filter(is_active=True)
            for warehouse in warehouses:
                incoming = InventoryTransaction.objects.filter(
                    product=product,
                    warehouse=warehouse,
                    transaction_type__in=['purchase', 'return_from_customer', 'adjustment_add']
                ).aggregate(total=Sum('quantity'))['total'] or 0

                outgoing = InventoryTransaction.objects.filter(
                    product=product,
                    warehouse=warehouse,
                    transaction_type__in=['sale', 'return_to_supplier', 'adjustment_subtract']
                ).aggregate(total=Sum('quantity'))['total'] or 0

                warehouse_stock = incoming - outgoing

                stock_data['warehouses'].append({
                    'warehouse_id': warehouse.id,
                    'warehouse_name': warehouse.name,
                    'stock': warehouse_stock
                })

            return Response(stock_data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

class WarehouseStockView(generics.RetrieveAPIView):
    """API view for retrieving warehouse stock information."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, warehouse_id):
        """Handle GET requests for warehouse stock."""
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
            products = Product.objects.filter(is_active=True)

            stock_data = {
                'warehouse_id': warehouse.id,
                'warehouse_name': warehouse.name,
                'products': []
            }

            for product in products:
                incoming = InventoryTransaction.objects.filter(
                    product=product,
                    warehouse=warehouse,
                    transaction_type__in=['purchase', 'return_from_customer', 'adjustment_add']
                ).aggregate(total=Sum('quantity'))['total'] or 0

                outgoing = InventoryTransaction.objects.filter(
                    product=product,
                    warehouse=warehouse,
                    transaction_type__in=['sale', 'return_to_supplier', 'adjustment_subtract']
                ).aggregate(total=Sum('quantity'))['total'] or 0

                product_stock = incoming - outgoing

                if product_stock > 0:
                    stock_data['products'].append({
                        'product_id': product.id,
                        'product_name': product.name,
                        'product_code': product.code,
                        'stock': product_stock,
                        'unit': product.unit.symbol
                    })

            return Response(stock_data)
        except Warehouse.DoesNotExist:
            return Response({'error': 'Warehouse not found'}, status=404)

class LowStockProductsView(generics.ListAPIView):
    """API view for listing products with low stock."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for low stock products."""
        low_stock_products = []

        for product in Product.objects.filter(is_active=True):
            if product.current_stock <= product.min_stock:
                low_stock_products.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_code': product.code,
                    'current_stock': product.current_stock,
                    'min_stock': product.min_stock,
                    'unit': product.unit.symbol
                })

        return Response(low_stock_products)
