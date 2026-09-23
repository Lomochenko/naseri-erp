from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F
from .models import Warehouse, InventoryTransaction, StockAdjustment, StockAdjustmentItem
from products.models import Product
from .serializers import (
    WarehouseSerializer, InventoryTransactionSerializer,
    StockAdjustmentSerializer, StockAdjustmentItemSerializer
)

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
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class StockAdjustmentItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing StockAdjustmentItem instances."""
    queryset = StockAdjustmentItem.objects.all()
    serializer_class = StockAdjustmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['adjustment', 'product']

class StockLevelsView(generics.ListAPIView):
    """API view to get current stock levels for all products."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryTransactionSerializer  # For swagger documentation
    queryset = Product.objects.none()  # Required for DRF but not used

    def list(self, request, *args, **kwargs):
        """Get current stock levels for all products using aggregated queries."""
        from django.db.models import Sum, Case, When, DecimalField
        from django.db.models.functions import Coalesce

        products = Product.objects.select_related('category', 'unit').filter(is_active=True)

        # Single query: aggregate all incoming transactions per product
        incoming_qs = InventoryTransaction.objects.filter(
            transaction_type__in=['purchase', 'return_from_customer', 'adjustment_add']
        ).values('product_id').annotate(total=Sum('quantity'))
        incoming_map = {r['product_id']: r['total'] for r in incoming_qs}

        # Single query: aggregate all outgoing transactions per product
        outgoing_qs = InventoryTransaction.objects.filter(
            transaction_type__in=['sale', 'return_to_supplier', 'adjustment_subtract']
        ).values('product_id').annotate(total=Sum('quantity'))
        outgoing_map = {r['product_id']: r['total'] for r in outgoing_qs}

        stock_data = []
        for product in products:
            current_stock = (incoming_map.get(product.id, 0) or 0) - (outgoing_map.get(product.id, 0) or 0)
            stock_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'product_code': product.code,
                'category_name': product.category.name if product.category else None,
                'unit_symbol': product.unit.symbol if product.unit else None,
                'current_stock': current_stock,
                'min_stock': float(product.min_stock),
                'max_stock': float(product.max_stock) if product.max_stock else 0,
                'is_low_stock': current_stock <= float(product.min_stock),
                'selling_price': float(product.selling_price),
                'purchase_price': float(product.purchase_price),
            })

        return Response(stock_data)

class ProductStockView(generics.RetrieveAPIView):
    """API view for retrieving product stock information."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryTransactionSerializer  # For swagger documentation

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
    serializer_class = WarehouseSerializer  # For swagger documentation

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
    serializer_class = InventoryTransactionSerializer  # For swagger documentation

    def get(self, request):
        """Handle GET requests for low stock products."""
        incoming_qs = InventoryTransaction.objects.filter(
            transaction_type__in=['purchase', 'return_from_customer', 'adjustment_add']
        ).values('product_id').annotate(total=Sum('quantity'))
        incoming_map = {r['product_id']: r['total'] for r in incoming_qs}

        outgoing_qs = InventoryTransaction.objects.filter(
            transaction_type__in=['sale', 'return_to_supplier', 'adjustment_subtract']
        ).values('product_id').annotate(total=Sum('quantity'))
        outgoing_map = {r['product_id']: r['total'] for r in outgoing_qs}

        low_stock_products = []
        for product in Product.objects.filter(is_active=True).select_related('unit'):
            current_stock = (incoming_map.get(product.id, 0) or 0) - (outgoing_map.get(product.id, 0) or 0)
            if current_stock <= float(product.min_stock):
                low_stock_products.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_code': product.code,
                    'current_stock': current_stock,
                    'min_stock': float(product.min_stock),
                    'unit': product.unit.symbol
                })

        return Response(low_stock_products)

class SimpleAdjustmentView(generics.CreateAPIView):
    """Simplified API view for creating stock adjustments."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StockAdjustmentSerializer  # For swagger documentation
    
    def post(self, request):
        """Handle POST requests for stock adjustments."""
        try:
            product_id = request.data.get('productId')
            adjustment_type = request.data.get('type')  # 'increase' or 'decrease'
            quantity = request.data.get('quantity')
            reason = request.data.get('reason', '')
            
            if not all([product_id, adjustment_type, quantity]):
                return Response({'error': 'Missing required fields'}, status=400)
            
            product = Product.objects.get(id=product_id)
            
            # Get or create default warehouse
            warehouse, created = Warehouse.objects.get_or_create(
                name='انبار اصلی',
                defaults={
                    'location': 'محل اصلی',
                    'description': 'انبار پیش‌فرض سیستم',
                    'is_active': True
                }
            )
            
            # Map frontend type to backend type
            backend_type = 'add' if adjustment_type == 'increase' else 'subtract'
            
            # Create the adjustment
            adjustment = StockAdjustment.objects.create(
                adjustment_type=backend_type,
                warehouse=warehouse,
                reason=reason,
                created_by=request.user
            )
            
            # Create the adjustment item
            StockAdjustmentItem.objects.create(
                adjustment=adjustment,
                product=product,
                quantity=quantity,
                notes=reason
            )
            
            return Response({
                'success': True,
                'message': 'تعدیل موجودی با موفقیت انجام شد',
                'adjustment_id': adjustment.id
            })
            
        except Product.DoesNotExist:
            return Response({'error': 'محصول یافت نشد'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
