from rest_framework import serializers
from .models import Customer, Sale, SaleItem, Invoice, Payment
from products.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'email', 'address', 'tax_number',
            'credit_limit', 'is_active', 'notes', 'created_at', 'updated_at',
            'total_due'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_due']

class SaleItemSerializer(serializers.ModelSerializer):
    """Serializer for SaleItem model."""
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')
    
    class Meta:
        model = SaleItem
        fields = [
            'id', 'sale', 'product', 'product_name', 'product_code',
            'quantity', 'unit_price', 'discount', 'notes'
        ]
        read_only_fields = ['id']

class SaleSerializer(serializers.ModelSerializer):
    """Serializer for Sale model."""
    customer_name = serializers.ReadOnlyField(source='customer.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    items = SaleItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Sale
        fields = [
            'id', 'invoice_number', 'customer', 'customer_name',
            'warehouse', 'warehouse_name', 'status', 'status_display',
            'sale_date', 'notes', 'discount_amount', 'tax_amount',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
            'items', 'subtotal', 'total'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'subtotal', 'total']

class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model."""
    customer_name = serializers.ReadOnlyField(source='customer.name')
    sale_invoice_number = serializers.ReadOnlyField(source='sale.invoice_number')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'customer', 'customer_name',
            'sale', 'sale_invoice_number', 'status', 'status_display',
            'issue_date', 'due_date', 'total_amount', 'paid_amount',
            'remaining_amount', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'remaining_amount']

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')
    customer_name = serializers.ReadOnlyField(source='invoice.customer.name')
    payment_method_display = serializers.ReadOnlyField(source='get_payment_method_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_number', 'invoice', 'invoice_number',
            'customer_name', 'amount', 'payment_method', 'payment_method_display',
            'payment_date', 'reference', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
