from rest_framework import serializers
from .models import Category, Unit, Product

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model."""
    
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    category_name = serializers.ReadOnlyField(source='category.name')
    unit_name = serializers.ReadOnlyField(source='unit.name')
    unit_symbol = serializers.ReadOnlyField(source='unit.symbol')
    current_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'barcode', 'name', 'description', 
            'category', 'category_name', 'unit', 'unit_name', 'unit_symbol',
            'purchase_price', 'selling_price', 'min_stock', 'current_stock',
            'is_active', 'image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_stock']

class ProductListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Product list view."""
    category_name = serializers.ReadOnlyField(source='category.name')
    unit_symbol = serializers.ReadOnlyField(source='unit.symbol')
    current_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'name', 'category_name', 
            'purchase_price', 'selling_price', 'current_stock',
            'unit_symbol', 'is_active'
        ]
