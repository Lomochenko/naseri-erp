from rest_framework import serializers
from .models import Warehouse, InventoryTransaction, StockAdjustment, StockAdjustmentItem
from products.serializers import ProductSerializer

class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for Warehouse model."""
    
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class InventoryTransactionSerializer(serializers.ModelSerializer):
    """Serializer for InventoryTransaction model."""
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    transaction_type_display = serializers.ReadOnlyField(source='get_transaction_type_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'transaction_type', 'transaction_type_display', 
            'product', 'product_name', 'product_code',
            'warehouse', 'warehouse_name', 'quantity', 'unit_price',
            'reference_number', 'reference_type', 'reference_id',
            'notes', 'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class StockAdjustmentItemSerializer(serializers.ModelSerializer):
    """Serializer for StockAdjustmentItem model."""
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')
    
    class Meta:
        model = StockAdjustmentItem
        fields = [
            'id', 'adjustment', 'product', 'product_name', 'product_code',
            'quantity', 'notes'
        ]
        read_only_fields = ['id']

class StockAdjustmentSerializer(serializers.ModelSerializer):
    """Serializer for StockAdjustment model."""
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    adjustment_type_display = serializers.ReadOnlyField(source='get_adjustment_type_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    items = StockAdjustmentItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = [
            'id', 'adjustment_type', 'adjustment_type_display',
            'warehouse', 'warehouse_name', 'reason',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
            'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
