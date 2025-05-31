from rest_framework import serializers
from .models import Supplier, Purchase, PurchaseItem, PurchaseInvoice, SupplierPayment
from products.serializers import ProductSerializer

class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model."""
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'phone', 'email', 'address',
            'tax_number', 'is_active', 'notes', 'created_at', 'updated_at',
            'total_due'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_due']

class PurchaseItemSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseItem model."""
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')
    
    class Meta:
        model = PurchaseItem
        fields = [
            'id', 'purchase', 'product', 'product_name', 'product_code',
            'quantity', 'received_quantity', 'unit_price', 'notes', 'total'
        ]
        read_only_fields = ['id', 'total']

class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase model."""
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    items = PurchaseItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id', 'reference_number', 'supplier', 'supplier_name',
            'warehouse', 'warehouse_name', 'status', 'status_display',
            'purchase_date', 'expected_receipt_date', 'notes',
            'discount_amount', 'tax_amount', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'items', 'subtotal', 'total'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'subtotal', 'total']

class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseInvoice model."""
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    purchase_reference = serializers.ReadOnlyField(source='purchase.reference_number')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = PurchaseInvoice
        fields = [
            'id', 'invoice_number', 'supplier', 'supplier_name',
            'purchase', 'purchase_reference', 'status', 'status_display',
            'issue_date', 'due_date', 'total_amount', 'paid_amount',
            'remaining_amount', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'remaining_amount']

class SupplierPaymentSerializer(serializers.ModelSerializer):
    """Serializer for SupplierPayment model."""
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')
    supplier_name = serializers.ReadOnlyField(source='invoice.supplier.name')
    payment_method_display = serializers.ReadOnlyField(source='get_payment_method_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = SupplierPayment
        fields = [
            'id', 'payment_number', 'invoice', 'invoice_number',
            'supplier_name', 'amount', 'payment_method', 'payment_method_display',
            'payment_date', 'reference', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
