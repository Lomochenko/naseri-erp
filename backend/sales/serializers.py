from rest_framework import serializers
from .models import Customer, Sale, SaleItem, Invoice, Payment
from products.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    
    class Meta:
        model = Customer
        fields = [
            'id', 'customer_code', 'name', 'phone', 'email', 'customer_type', 'business_category',
            'address', 'tax_number', 'credit_limit', 'is_active', 'notes',
            'created_at', 'updated_at', 'total_due', 'account_balance'
        ]
        read_only_fields = ['id', 'customer_code', 'created_at', 'updated_at', 'total_due', 'account_balance']

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
        read_only_fields = ['id', 'sale', 'product_name', 'product_code']

class SaleCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Sale model."""
    items = SaleItemSerializer(many=True, write_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'customer', 'status', 'sale_date',
            'notes', 'discount_amount', 'tax_amount', 'items'
        ]
        read_only_fields = ['id']

    def validate_customer(self, value):
        """Validate customer exists."""
        if not value:
            raise serializers.ValidationError("Customer is required")
        return value

    def validate_items(self, value):
        """Validate items."""
        if not value:
            raise serializers.ValidationError("At least one item is required")

        for item in value:
            if not item.get('product'):
                raise serializers.ValidationError("Product is required for each item")
            if not item.get('quantity') or float(item.get('quantity', 0)) <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
            if item.get('unit_price') is None or float(item.get('unit_price', 0)) < 0:
                raise serializers.ValidationError("Unit price must be 0 or greater")

        return value

    def create(self, validated_data):
        """Create sale with ERP integration."""
        print(f"=== CREATING SALE ===")
        print(f"Validated data: {validated_data}")

        from django.db import transaction
        from inventory.models import Warehouse

        items_data = validated_data.pop('items', [])
        print(f"Items count: {len(items_data)}")

        # Get user from context
        user = self.context['request'].user
        validated_data['created_by'] = user

        # Auto-assign warehouse
        if not validated_data.get('warehouse'):
            default_warehouse = Warehouse.objects.filter(is_active=True).first()
            if default_warehouse:
                validated_data['warehouse'] = default_warehouse
                print(f"Auto-assigned warehouse: {default_warehouse.name}")

        try:
            with transaction.atomic():
                # Create sale
                sale = Sale.objects.create(**validated_data)
                print(f"Sale created: {sale.id}")

                # Create items
                for item_data in items_data:
                    SaleItem.objects.create(sale=sale, **item_data)
                    print(f"Item created: {item_data['product']}")

                return sale

        except Exception as e:
            print(f"Error: {str(e)}")
            raise

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        # Update sale fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update items
        instance.items.all().delete()
        for item_data in items_data:
            SaleItem.objects.create(sale=instance, **item_data)

        return instance

class SaleSerializer(serializers.ModelSerializer):
    """Serializer for Sale model (read-only)."""
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
